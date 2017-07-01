from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from appauth.api_authentication import SessionAuthenticationAllMethods, CsrfExemptSessionAuthentication
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
            product.is_active = False
            product.save()
        return Response(
            ResponseHandler.get_result(SuccesMessages.PRODUCT_ASSIGNED.value),
            status=status.HTTP_200_OK)


class ProductDropAPI(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        product_id = request.data.get(RequestKeys.PRODUCT_ID.value, None)
        try:
            product = Products.objects.get(code=product_id)
        except Products.DoesNotExist:
            return Response(
                ResponseHandler.get_result(FailureMessages.INVALID_INPUT.value), status=status.HTTP_200_OK)
        if not product.is_active:
            user_product = UserProducts.objects.get(product=product)
            if user_product.status == UserProducts.PRODUCT_STATUS[0][0]:
                new_user_point = UserProducts.calculate_user_points(user_product)
                user_product.status = UserProducts.PRODUCT_STATUS[2][0]
                user_product.save()
                return Response(
                    ResponseHandler.get_result(SuccesMessages.PRODUCT_REDEEMED.value % new_user_point),
                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(ResponseHandler.get_result(FailureMessages.CORRUPTED_PRODUCT.value),
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(ResponseHandler.get_result(FailureMessages.INACTIVE_PRODUCT.value),
                            status=status.HTTP_400_BAD_REQUEST)
