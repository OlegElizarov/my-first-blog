from django.conf.urls import *
from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^admin/', admin.site.urls ),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]