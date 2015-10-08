from datetime import timedelta
from django.utils import timezone
from django.test import LiveServerTestCase
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from django.core import mail
from django.contrib.auth.models import User
from accounts.models import UserProfile


class TestSignup(LiveServerTestCase):
    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND='memory')
    def test_signup(self):
        url = reverse('signup', kwargs={'step': 'user'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A verification token will be sent to the above number by SMS')
        
        data = {'signup_wizard-current_step': 'user', 'user-username': 'evanson',
                'user-first_name': 'Evanson', 'user-last_name': 'Wachira',
                'user-password1': 'evanson', 'user-password2': 'evanson',
                'user-email': 'evansonwachira@gmail.com',
                'user-country_code': '+254',
                'user-phone_number': '725911243',}
        response = self.client.post(url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'If you did not receive the token, please go back to the previous step and verify your number is correct')
        verification_url = reverse('signup', kwargs={'step': 'token'})
        verification_data = {'signup_wizard-current_step': 'token',
                             'token-token': self.client.session['generated_token']}
        response = self.client.post(verification_url, data=verification_data,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You've successfully signed up.")
        
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Account Confirmation')
        
    
class TestLogin(LiveServerTestCase):
    def setUp(self):
        testuser = User.objects.create_user(username='evanson', password='evanson', email='evanson@expressprepaid.co')
        UserProfile.objects.create(user=testuser, phone_number='+254725911243',
                                   activation_key='randomiyu7yeuy282',
                                   key_expires=(timezone.now()+timedelta(days=1)))

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND='memory')
    def test_login(self):
        url = reverse('login', kwargs={'step': 'user'})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A verification token will be sent')

        data = {'login_wizard-current_step': 'user', 'user-username': 'evanson',
                'user-password': 'wrongpassword'}
        response = self.client.post(url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')
        
        data = {'login_wizard-current_step': 'user', 'user-username': 'evanson',
                'user-password': 'evanson'}
        response = self.client.post(url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please input the token sent to your phone number')

        token_url = reverse('login', kwargs={'step': 'token'})
        token_data = {'login_wizard-current_step': 'token', 'token-token': self.client.session['login_token']}
        response = self.client.post(token_url, data=token_data, follow=True)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(username='evanson')
        self.assertContains(response, user.userprofile.phone_number)
