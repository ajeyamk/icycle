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
from django.conf import settings

from .views import IndexView, health
from django.contrib import admin

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Project API')

v1 = settings.VERSION['v1']


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^api/$', schema_view, name='swagger'),
    url(r'^health/$', health, name='health'),

    # --- Appauth
    url(r'^api/%s/auth/' % v1, include('appauth.api_urls', namespace='appauth_api')),

    # --- Posts
    url(r'^posts/', include('posts.urls', namespace='posts')),
    url(r'^api/%s/posts/' % v1, include('posts.api_urls', namespace='posts_api')),

    # --- Errorlog
    url(r'^logs/', include('logger.urls', namespace='logger')),
]
