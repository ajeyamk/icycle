from django.conf.urls import url

from .api_views import (
    TestAPILogs,
)

urlpatterns = [
    url(r'^api/test/$', TestAPILogs.as_view(), name='api_test'),
]
