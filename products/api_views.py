import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from appauth.api_authentication import AdminAuthenticationAllMethods
from product_categories.models import Categories
from products.constants import RequestKeys, SuccesMessages, FailureMessages
from products.models import Products
from utils.response_handler import ResponseHandler


class GenerateProductsAPI(APIView):
    """
    An API for creating products codes, tied to Django admin
    """
    authentication_classes = (AdminAuthenticationAllMethods,)

    def post(self, request):
        cat_type_id = request.data.get(RequestKeys.CATEGORY_TYPE.value, None)
        no_of_products = request.data.get(RequestKeys.NUMBER_OF_PRODUCTS.value, None)
        if cat_type_id and no_of_products:
            cat_type = Categories.objects.get(id=cat_type_id)
            products = [
                Products(
                    category=cat_type,
                    code=str(uuid.uuid4())) for i in range(no_of_products)
                ]
            Products.objects.bulk_create(products)
            return Response(
                ResponseHandler.get_result(SuccesMessages.PRODUCTS_GENERATED.value % no_of_products),
                status=status.HTTP_200_OK)
        else:
            return Response(
                ResponseHandler.get_result(FailureMessages.INVALID_INPUT.value), status=status.HTTP_400_BAD_REQUEST)
