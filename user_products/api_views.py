from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from appauth.api_authentication import SessionAuthenticationAllMethods, CsrfExemptSessionAuthentication
from product_categories.models import Categories
from products.models import Products
from user_products.constants import RequestKeys, FailureMessages, SuccesMessages, ResponseKeys
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
        if UserProducts.objects.filter(product=product, status=UserProducts.PRODUCT_STATUS[0][0]).exists():
            return Response(
                ResponseHandler.get_result(FailureMessages.USER_ALREADY_LINKED.value),
                status=status.HTTP_400_BAD_REQUEST)
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
                ResponseHandler.get_result(FailureMessages.INVALID_INPUT.value), status=status.HTTP_400_BAD_REQUEST)
        if not product.is_active:
            user_product = UserProducts.objects.get(product=product)
            if user_product.status == UserProducts.PRODUCT_STATUS[0][0]:
                new_user_point = UserProducts.calculate_user_points(user_product)
                user_product.status = UserProducts.PRODUCT_STATUS[2][0]
                user_product.save()
                product.is_active = True
                product.save()
                return Response(
                    ResponseHandler.get_result(SuccesMessages.PRODUCT_REDEEMED.value % new_user_point),
                    status=status.HTTP_200_OK)
            else:
                return Response(ResponseHandler.get_result(FailureMessages.CORRUPTED_PRODUCT.value),
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(ResponseHandler.get_result(FailureMessages.INACTIVE_PRODUCT.value),
                            status=status.HTTP_400_BAD_REQUEST)


class Dashboard(APIView):
    authentication_classes = (SessionAuthenticationAllMethods,)

    def get(self, request):
        resultNode = {}
        resultNode[ResponseKeys.USER_POINTS.value] = request.user.user_point
        purchased_query = UserProducts.objects.filter(user=request.user, status=UserProducts.PRODUCT_STATUS[0][0])
        resultNode[ResponseKeys.TOTAL_ACTIVE_COUNT.value] = purchased_query.count()
        purchased_products = purchased_query.values('product_id')
        completed_query = UserProducts.objects.filter(user=request.user, status=UserProducts.PRODUCT_STATUS[2][0])
        resultNode[ResponseKeys.TOTAL_COMPLETED_COUNT.value] = completed_query.count()
        completed_products = completed_query.values('product_id')
        completed_ids = []
        active_ids = []
        for each_node in completed_products:
            completed_ids.append(each_node['product_id'])
        for each_purchased_node in purchased_products:
            active_ids.append(each_purchased_node['product_id'])
        data_node = []
        data = {}
        for i in Categories.CATEGORY_TYPES:
            data[ResponseKeys.ID.value] = i[0]
            data[ResponseKeys.COMPLETED_COUNT.value] = Products.objects.filter(id__in=completed_ids,
                                                                               category_id=i[0]).count()
            data[ResponseKeys.ACTIVE_COUNT.value] = Products.objects.filter(id__in=active_ids, category_id=i[0]).count()
            data_node.append(data)
            data = {}
        resultNode[ResponseKeys.CATEGORIES.value] = data_node
        return Response(resultNode, status=status.HTTP_200_OK)


class RedeemCoupoun(APIView):
    authentication_classes = (SessionAuthenticationAllMethods,)

    def get(self, request):
        if request.user.user_point >= 50.0:
            request.user.user_point = 0
            request.user.save()
            return Response(
                ResponseHandler.get_result(SuccesMessages.REDEEM_MESSAGE.value % request.user.first_name),
                status=status.HTTP_200_OK)
        else:
            return Response(ResponseHandler.get_result(FailureMessages.INVALID_INPUT.value),
                            status=status.HTTP_400_BAD_REQUEST)
