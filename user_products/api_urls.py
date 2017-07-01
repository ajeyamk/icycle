from django.conf.urls import url

from .api_views import (
    PurchaseProductAPI

)

urlpatterns = [
    url(r'^assign/$', PurchaseProductAPI.as_view(), name='assign-product'),
]
