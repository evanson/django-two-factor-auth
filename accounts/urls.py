from django.conf.urls import patterns, url
import accounts
from views import SignupWizard, SIGNUP_FORMS, LoginWizard, LOGIN_FORMS

signup_wizard = SignupWizard.as_view(SIGNUP_FORMS, url_name='signup',
                                     done_step_name='done')

login_wizard = LoginWizard.as_view(LOGIN_FORMS, url_name='login',
                                     done_step_name='done')


urlpatterns = patterns(
    '',
    url(r'^signup/(?P<step>.+)$', signup_wizard, name='signup'),
    url(r'^confirm/(?P<activation_key>\w+)/', 'accounts.views.signup_confirm', name='email_confirm'),
    url(r'^login/(?P<step>.+)/$', login_wizard, name='login'),
    url(r'^logout/$', 'accounts.views.end_session', name='logout'),
    url(r'^profile/$', 'accounts.views.user_profile', name='profile'),
)
