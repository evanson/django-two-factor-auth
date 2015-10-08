from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phone_number = models.CharField(max_length=20)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return self.user.get_full_name()
