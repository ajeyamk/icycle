from django.conf.urls import url

from .api_views import (
    LoginAPI,
    LogoutAPI,
)

urlpatterns = [
    url(r'^login/$', LoginAPI.as_view(), name='login'),
    url(r'^logout/$', LogoutAPI.as_view(), name='logout'),
]
