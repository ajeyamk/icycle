from django.conf.urls import url

from .api_views import (
    PurchaseProductAPI,
    ProductDropAPI,
    Dashboard,
)

urlpatterns = [
    url(r'^assign/$', PurchaseProductAPI.as_view(), name='assign-product'),
    url(r'^return/$', ProductDropAPI.as_view(), name='drop-product'),
    url(r'^dashboard/$', Dashboard.as_view(), name='dashboard'),

]
