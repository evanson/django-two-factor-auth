from __future__ import absolute_import

from twilio.rest import TwilioRestClient
from django.conf import settings


client = TwilioRestClient(account=settings.TWILIO_ACCOUNT_SID,
                          token=settings.TWILIO_AUTH_TOKEN)
