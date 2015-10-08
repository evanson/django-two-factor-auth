import re
import random
import logging
import hashlib
import marshal
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils import timezone
from django.contrib.formtools.wizard.views import NamedUrlSessionWizardView
from django.contrib.auth.models import User
from django.db import transaction
from django.conf import settings

from models import UserProfile
from forms import CreateUserForm, TokenForm, LoginForm
from tasks import send_sms, send_email


def server_error(request, msg=None):
    if msg is None:
        msg = "Sorry! We screwed up. We're looking into it"
    print "server_error: %s" %(msg)
    messages.error(request, msg)
    tmpl_messages = messages.get_messages(request)
    return render_to_response('500.html', {'messages': tmpl_messages})
    

def index(request):
    try:
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('profile'))
        return render(request, 'index.html', {})
    except Exception, e:
        logging.exception(e)


def generate_token():
    timestamp = datetime.now()
    t_id = str(timestamp)[2:]
    t = '1' + str(re.sub("[^0-9]","",t_id))
    token = str(int(random.random() * int(t)))[:5]
    return token
    

SIGNUP_FORMS = (
    ('user', CreateUserForm),
    ('token', TokenForm),
)

SIGNUP_TEMPLATES = {
    'user': 'accounts/signup.html',
    'token': 'accounts/token.html',
}


class SignupWizard(NamedUrlSessionWizardView):
    def __init__(self, *args, **kwargs):
        super(SignupWizard, self).__init__(*args, **kwargs)
        self.initial_dict = {"user": {"country_code": "+254"}}

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('profile'))
        return super(SignupWizard, self).dispatch(*args, **kwargs)

    def get_template_names(self):
        return [SIGNUP_TEMPLATES[self.steps.current]]

    def get_form_kwargs(self, step=None):
        if step=='token':
            return {'gen_token': self.request.session['generated_token']}
        return {}

    def process_step(self, form):
        if 'user-phone_number' in form.data:
            phone_number = form.data['user-country_code'] + form.data['user-phone_number']
            token = generate_token()
            self.request.session['generated_token'] = token
            msg = "Verification token: {}".format(token)
            send_sms.delay(msg, phone_number)
        return self.get_form_step_data(form)
        
    def done(self, form_list, form_dict, **kwargs):
        with transaction.atomic():
            user_data = form_dict['user'].cleaned_data
            phone_number = user_data['country_code'] + user_data['phone_number']
            email = user_data['email']
            username = user_data['username']
            
            user = form_dict['user'].save()

            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha1(salt+email).hexdigest()
            key_expires = timezone.now() + timedelta(days=30)

            user_profile = UserProfile(user=user, phone_number=phone_number,
                                       activation_key=activation_key,
                                       key_expires=key_expires)
            user_profile.save()

            email_subject = 'Account Confirmation'
            confirmation_url = self.request.build_absolute_uri(reverse('email_confirm',
                                                                       kwargs={'activation_key': activation_key}))
            email_body = "Hello %s, thanks for signing up. To activate your account,\
click this link %s" % (username, confirmation_url)

            send_email.delay(email_subject, email_body, [email])
            messages.success(self.request, "You've successfully signed up. Please click the activation link sent to your email to activate your account")
            return HttpResponseRedirect('/')


def signup_confirm(request, activation_key):
    try:
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')

        user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
        if user_profile.key_expires < timezone.now():
            messages.error(request, "Your account confirmation period has expired")
            return HttpResponseRedirect('/')
        user = user_profile.user
        user.is_active = True
        user.save()
        messages.success(request, "You've successfully activated your account")
        return HttpResponseRedirect(reverse('login', kwargs={'step': 'user'}))
    except ObjectDoesNotExist:
        return Http404()
    except Exception, e:
        logging.exception(e)
        return server_error(request)


LOGIN_FORMS = (
    ('user', LoginForm),
    ('token', TokenForm),
)

LOGIN_TEMPLATES = {
    'user': 'accounts/login.html',
    'token': 'accounts/token.html',
}


class LoginWizard(NamedUrlSessionWizardView):
            
    def get_template_names(self):
        return [LOGIN_TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super(LoginWizard, self).get_context_data(form=form, **kwargs)
        if self.steps.current == "token":
            context.update({'login': True})

        return context

    def get_form_kwargs(self, step=None):
        if step=='token':
            return {'gen_token': self.request.session['login_token']}
        return {}

    def process_step(self, form):
        if 'user-username' in form.data:
            user = authenticate(username=form.data['user-username'], password=form.data['user-password'])
            user_profile = UserProfile.objects.get(user=user)
            phone_number = user_profile.phone_number
            token = generate_token()
            self.request.session['login_token'] = token
            msg = "Verification token: {}".format(token)
            send_sms.delay(msg, phone_number)
        return self.get_form_step_data(form)
        
    def done(self, form_list, form_dict, **kwargs):
        username, password = form_dict['user'].cleaned_data['username'], form_dict['user'].cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect(reverse('profile'))


def end_session(request):
    logout(request)
    return HttpResponseRedirect(reverse('login', kwargs={'step': 'user'}))


@login_required(login_url=reverse_lazy('login', kwargs={'step': 'user'}))
def user_profile(request):
    try:
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        return render(request, 'accounts/profile.html', {'user': user,
                                                         'user_profile': user_profile})
    except Exception, e:
        logging.exception(e)
        return server_error(request)
