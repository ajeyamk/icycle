from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError

from utils.response_handler import ResponseHandler
from .serializers import (
    AppUserSerializer,
)
from .constants import (
    ResponseKeys,
    FailureMessages, RequestKeys)
from .api_authentication import (
    CsrfExemptSessionAuthentication,
)


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

    def post(self, request):
        """
        # API through which a user can login.

        Logs a user in. Creates a session and sends back the session token along with user data.
        This token is expected for all authenticated APIs.

        **Header**:

            {
                "Content-Type": "application/json"
            }

        **Data**:

            {
                "username": "eshan@scientist-tech.com",
                "password": "abc123"
            }
        """
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    request.session.save()
                    serializer = self.serializer_class(user)
                    context = {
                        ResponseKeys.SESSION_ID: request.session.session_key,
                        ResponseKeys.USER: serializer.data}
                    return Response(
                        context,
                        status=status.HTTP_200_OK)
                else:
                    return Response(
                        generic_response(FailMessages.USER_INACTIVE),
                        status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    generic_response(FailMessages.INVALID_CREDENTIALS),
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                generic_response(FailMessages.INVALID_CREDENTIALS),
                status=status.HTTP_400_BAD_REQUEST)


class LogoutAPI(APIView):
    def post(self, request):
        context = {"loggedOut": True}
        return Response(
            context,
            status=status.HTTP_200_OK)
