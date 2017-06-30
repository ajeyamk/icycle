from django.conf.urls import url

from .api_views import (
    LoginAPI,
    LogoutAPI,
    RegisterUser
)

urlpatterns = [
    url(r'^register/$', RegisterUser.as_view(), name='register'),
    url(r'^login/$', LoginAPI.as_view(), name='login'),
    url(r'^logout/$', LogoutAPI.as_view(), name='logout'),
]
