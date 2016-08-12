from django.utils.crypto import get_random_string

from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView

from django.contrib.auth import authenticate, login, logout
from appauth.models import AppUser
from appauth.serializers import AppUserSerializer

from utils.email.email_templates.appauth import (
    ForgotPasswordEmail,
    PasswordChangeSuccessEmail,
    PasswordChangeFailEmail,
)
from utils.email.email_tasks import send_async_system_email

from .api_authentication import SessionAuthenticationAllMethods


class LoginUserAPI(APIView):
    """
    An API for logging in a user.
    """
    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        if email and password:
            email = email.lower()
            active_user = AppUser.objects.get(email=email, is_active=True)
            if active_user:
                user = authenticate(email=email, password=password)
                if user is not None:
                    login(request, user)
                    return Response({'success': True, 'user': user.name}, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {'success': False, 'message': 'Incorrect password'},
                        status=status.HTTP_406_NOT_ACCEPTABLE)
                return Response(
                    {'success': False, 'message': 'Incomplete data'},
                    status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return Response(
                    {'success': False, 'message': 'User Inactive'},
                    status=status.HTTP_200_OK)
        else:
            return Response(
                {'success': False, 'message': 'Invalid password'},
                status=status.HTTP_200_OK)


class LogoutUserAPI(APIView):
    """
    An API for logging out a user.
    """
    authentication_classes = (SessionAuthenticationAllMethods, )

    def get(self, request):
        logout(request)
        return Response(
            {'success': True, 'message': 'User has been logged out'},
            status=status.HTTP_200_OK)


class TestAPI(APIView):
    """
    A test API to confirm everything is working fine or not.
    """
    authentication_classes = (SessionAuthenticationAllMethods, )

    def post(self, request):
        key1 = request.data.get('key1', '')
        key2 = request.data.get('key2', '')
        return Response(
            {'message': 'Your data %s %s' % (key1, key2)},
            status=status.HTTP_200_OK)


class ForgotPasswordAPI(APIView):
    """
    An API to recover an account's password.
    Reset the password and email the new password to the email id.
    """
    def get(self, request):
        email = request.GET.get('email', None)
        if email:
            try:
                token = get_random_string(length=8)
                user = AppUser.objects.get(email=email)
                if user.is_active:
                    user = AppUser.objects.filter(email=email, is_active=True).update(reset_password_token=token)
                    # Sending email before returning
                    forgot_password_email = ForgotPasswordEmail()
                    forgot_password_email.message = forgot_password_email.message % token
                    forgot_password_email.recipient_list = [email]
                    forgot_password_email.context = {'new_password': token}
                    send_async_system_email.delay(forgot_password_email)
                    return Response(
                        {'success': True, 'message': 'Secret token has been mailed'},
                        status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(
                        {'success': False, 'message': 'This user is not active'},
                        status=status.HTTP_400_BAD_REQUEST)
            except AppUser.DoesNotExist:
                return Response(
                    {'success': False, 'message': 'The user with this email does not exist'},
                    status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPI(APIView):
    """
    An API which resets old password with the newly provided password.
    It also logs in and creates a session for the user.

    data = [{
            "email":"professory@mailinator.com",
            "oldPassword":"6vlOtmWc",
            "password":"professorx"
        }]
    """
    def post(self, request):
        email = request.data.get('email', None)
        old_password = request.data.get('oldPassword', None)
        password = request.data.get('password', None)
        if email and password and old_password:
            user = authenticate(email=email, password=old_password)
            if user is not None:
                try:
                    user = AppUser.objects.get(email=email)
                    user.set_password(password)
                    user.is_verified = True
                    user.save()
                    user = authenticate(email=email, password=password)
                    if user is not None:
                        login(request, user)
                        # Sending email before returning
                        password_change_success_email = PasswordChangeSuccessEmail()
                        password_change_success_email.recipient_list = [email]
                        send_async_system_email.delay(password_change_success_email)
                        return Response(
                            {'success': True, 'message': 'Password changed successfully'},
                            status=status.HTTP_200_OK)
                    else:
                        # Sending email before returning
                        password_change_fail_email = PasswordChangeFailEmail()
                        password_change_fail_email.recipient_list = [email]
                        send_async_system_email.delay(password_change_fail_email)
                        return Response(
                            {'success': False, 'message': 'Incorrect password'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

                except AppUser.DoesNotExist:
                    # Sending email before returning
                    password_change_fail_email = PasswordChangeFailEmail()
                    password_change_fail_email.recipient_list = [email]
                    send_async_system_email.delay(password_change_fail_email)
                    return Response(
                        {'success': False, 'message': 'Invalid email'},
                        status=status.HTTP_200_OK)
            else:
                # Sending email before returning
                password_change_fail_email = PasswordChangeFailEmail()
                password_change_fail_email.recipient_list = [email]
                send_async_system_email.delay(password_change_fail_email)
                return Response(
                    {'success': False, 'message': 'Invalid current password'},
                    status=status.HTTP_200_OK)

        # Sending email before returning
        password_change_fail_email = PasswordChangeFailEmail()
        password_change_fail_email.recipient_list = [email]
        send_async_system_email.delay(password_change_fail_email)
        return Response(
            {'success': False, 'message': 'Invalid email or password'},
            status=status.HTTP_200_OK)


class GetAllUsersAPI(APIView):
    """
    Fetches all the Users. Inherits GetAllAPI class.
    """
    authentication_classes = (SessionAuthenticationAllMethods, )

    def get(self, request):
        users = AppUser.objects.all()
        serializer = AppUserSerializer(users, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK)
