from django.conf.urls import url

from .views import (
    AllLogs,
    AllRequestLogs,
    TestLogs,
    TestRequestLogs,
)

urlpatterns = [
    url(r'^all/$', AllLogs.as_view(), name='all_logs'),
    url(r'^request/all/$', AllRequestLogs.as_view(), name='all_request_logs'),
    url(r'^test/$', TestLogs.as_view(), name='test'),
    url(r'^request/test/$', TestRequestLogs.as_view(), name='request_test'),
]
