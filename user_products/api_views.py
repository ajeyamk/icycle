from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from appauth.api_authentication import SessionAuthenticationAllMethods
from products.models import Products
from user_products.constants import RequestKeys, FailureMessages, SuccesMessages
from user_products.models import UserProducts
from utils.response_handler import ResponseHandler


class PurchaseProductAPI(APIView):
    """
    An API for creating products codes, tied to Django admin
    """
    authentication_classes = (SessionAuthenticationAllMethods,)

    def post(self, request):
        product_id = request.data.get(RequestKeys.PRODUCT_ID.value, None)
        try:
            product = Products.objects.get(code=product_id)
        except Products.DoesNotExist:
            return Response(
                ResponseHandler.get_result(FailureMessages.INVALID_INPUT.value), status=status.HTTP_400_BAD_REQUEST)
        if not product.is_active:
            return Response(
                ResponseHandler.get_result(FailureMessages.PRODUCT_IN_USE.value), status=status.HTTP_400_BAD_REQUEST)
        else:
            UserProducts.add(request.user, product)
        return Response(
            ResponseHandler.get_result(SuccesMessages.PRODUCT_ASSIGNED.value),
            status=status.HTTP_200_OK)
