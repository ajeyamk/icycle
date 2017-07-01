from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError

from utils.response_handler import ResponseHandler
from .serializers import (
    AppUserSerializer,
)
from .constants import (
    ResponseKeys,
    FailureMessages, RequestKeys, SuccesMessages)
from .api_authentication import (
    CsrfExemptSessionAuthentication,
    SessionAuthenticationAllMethods)


class RegisterUser(APIView):
    """
    API for user registration
    """
    authentication_classes = (CsrfExemptSessionAuthentication,)
    serializer_class = AppUserSerializer

    def post(self, request):
        if any(request.data):
            serializer = self.serializer_class(data=request.data)
            password = request.data.get(RequestKeys.PASSWORD.value)
            if serializer.is_valid():
                user = serializer.save()
                user.set_password(password)
                user.save()
                try:
                    user.full_clean()
                except ValidationError as e:
                    return Response(ResponseHandler.get_result(FailureMessages.TECHNICAL_ERROR.value),
                                    status=status.HTTP_400_BAD_REQUEST)
                login(request, user)
                request.session.save()
                context = {
                    ResponseKeys.USER.value: serializer.data,
                    ResponseKeys.SESSION_ID.value: request.session.session_key}
                return Response(context, status=status.HTTP_200_OK)
            else:
                return Response(ResponseHandler.get_result(dict(serializer.errors).values()[0]),
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(ResponseHandler.get_result(FailureMessages.INVALID_INPUT.value),
                            status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(APIView):
    serializer_class = AppUserSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        email = request.data.get(RequestKeys.EMAIL.value, None)
        password = request.data.get(RequestKeys.PASSWORD.value, None)
        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                request.session.save()
                serializer = self.serializer_class(user)
                context = {
                    ResponseKeys.SESSION_ID.value: request.session.session_key,
                    ResponseKeys.USER.value: serializer.data}
                return Response(
                    context,
                    status=status.HTTP_200_OK)
            else:
                return Response(
                    ResponseHandler.get_result(FailureMessages.INVALID_CREDENTIALS.value),
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                ResponseHandler.get_result(FailureMessages.INVALID_INPUT.value),
                status=status.HTTP_400_BAD_REQUEST)


class LogoutAPI(APIView):
    """
    An API for logging out a user.
    """
    authentication_classes = (SessionAuthenticationAllMethods,)

    def delete(self, request):
        logout(request)
        return Response(
            ResponseHandler.get_result(SuccesMessages.USER_LOGGED_OUT.value),
            status=status.HTTP_200_OK)
