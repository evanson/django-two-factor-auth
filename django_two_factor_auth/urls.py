from django.conf.urls import patterns, include, url
from django.contrib import admin

import accounts

urlpatterns = patterns(
    '',
    url(r'^$', 'accounts.views.index', name='index'),
    url(r'^accounts/', include('accounts.urls')),
)
