"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings

from .views import home, health

v1 = settings.VERSION['v1']

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^health/$', health, name='health'),

    # --- Admin Urls --- #
    url(r'^admin/', include(admin.site.urls)),

    # --- Errors Urls --- #
    url(r'^auth/', include('appauth.urls', namespace='appauth')),
    url(r'^api/%s/auth/' % v1, include('appauth.api_urls', namespace='appauth_api')),

    # --- Errors Urls --- #
    url(r'^errors/', include('errorlog.urls', namespace='errorlog')),
]
