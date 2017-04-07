from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate, login, logout

from utils.response_handler import generic_response

from .serializers import (
    AppUserSerializer,
)

from .constants import (
    FailMessages,
    ResponseKeys,
)


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
        """
        # API through which a user can logout.

        Logs a user out. Destroys the session.

        **Header**:

            {
                "Content-Type": "application/json",
                "sessionId": "token"
            }
        """
        context = {"loggedOut": True}
        return Response(
            context,
            status=status.HTTP_200_OK)
