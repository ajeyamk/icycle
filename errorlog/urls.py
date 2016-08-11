from django.conf.urls import url

from .views import (
    GetAllErrors,
    delete_all_errors,
)

urlpatterns = [
    url(r'^all/$', GetAllErrors.as_view(), name='all_errors'),
    url(r'^delete/$', delete_all_errors, name='delete_all'),
]
