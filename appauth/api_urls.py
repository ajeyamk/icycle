from django.conf.urls import url
from .api_views import (
    LoginUserAPI,
    LogoutUserAPI,
    TestAPI,
    ForgotPasswordAPI,
    ResetPasswordAPI,
    GetAllUsersAPI,
)


urlpatterns = [
    url(r'^login/$', LoginUserAPI.as_view(), name='login_api'),
    url(r'^logout/$', LogoutUserAPI.as_view(), name='logout_api'),
    url(r'^test/$', TestAPI.as_view(), name='test_api'),
]
