from __future__ import absolute_import
import marshal, types
import logging
from django.core.mail import send_mail
from django.conf import settings
from django_two_factor_auth import app
from django_two_factor_auth import twilio_client


@app.task
def send_sms(text, recipient):
    try:
        logging.info("Sending message '{}' to {}".format(text, recipient))
        message = twilio_client.messages.create(body=text, to=recipient,
                                         from_=settings.TWILIO_FROM_NUMBER)
        logging.info("SMS ID: {}".format(message.sid))
    except Exception, e:
        logging.exception(e)
        return False
    return True


@app.task
def send_email(subject, message, recipients):
    try:
        logging.info("Sending message '{}' to {}".format(message, recipients))
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipients,
                  fail_silently=False)
    except Exception, e:
        logging.exception(e)
        return False
    return True
