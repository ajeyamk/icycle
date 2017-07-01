from django.conf.urls import url

from .api_views import (
    PurchaseProductAPI,
    ProductDropAPI,
    Dashboard,
    RedeemCoupoun,
)

urlpatterns = [
    url(r'^assign/$', PurchaseProductAPI.as_view(), name='assign-product'),
    url(r'^return/$', ProductDropAPI.as_view(), name='drop-product'),
    url(r'^dashboard/$', Dashboard.as_view(), name='dashboard'),
    url(r'^redeem-coupon/$', RedeemCoupoun.as_view(), name='redeem-coupon'),

]
