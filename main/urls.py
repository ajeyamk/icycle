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
from .api_views import PingCelery
from django.contrib import admin

from django_rest_swagger_enhancer.schema_generator import get_swagger_view, CustomSchemaGenerator

schema_view = get_swagger_view(title='Django iCycle', generator_class=CustomSchemaGenerator)

v1 = settings.VERSION['v1']

admin.site.site_header = 'Django iCycle'

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^api/$', schema_view, name='swagger'),
    url(r'^health/$', health, name='health'),
    url(r'^ping-celery/', PingCelery.as_view(), name='ping_celery'),

    # --- Appauth
    url(r'^api/auth/', include('appauth.api_urls', namespace='appauth_api')),

    # --- Products
    url(r'^api/products/', include('products.api_urls', namespace='products')),

    # --- Errorlog
    url(r'^logs/', include('simple_django_logger.urls', namespace='logger')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
