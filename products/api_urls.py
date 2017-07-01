from django.conf.urls import url

from .api_views import (
    GenerateProductsAPI

)

urlpatterns = [
    url(r'^generate/$', GenerateProductsAPI.as_view(), name='generate-products'),
]
