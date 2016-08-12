from django.contrib.sessions.backends.db import SessionStore
from .models import AppUser

from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.permissions import SAFE_METHODS


def getSessionId(request):
    session_id = request.COOKIES.get('sessionid', '')
    if not session_id:
        session_id = request.META.get('HTTP_SESSIONID', '')
        if not session_id:
            raise exceptions.AuthenticationFailed('Invalid session id')
    return session_id


class SessionAuthenticationUnsafeMethods(authentication.BaseAuthentication):
    """
    Session Id is expected only for UNSAFE methods, i.e: PUT, POST, DELETE
    SAFE_METHODS get free passage and Session Id is not checked.
    """
    def authenticate(self, request):
        if request.method in SAFE_METHODS:
            return (None, None)

        session_id = getSessionId(request)
        sessionStore = SessionStore(session_key=session_id)
        uid = sessionStore.get('_auth_user_id', '')

        # Add the session object into request
        request.session = sessionStore

        if not uid:
            raise exceptions.AuthenticationFailed('Invalid session id')
        try:
            user = AppUser.objects.get(id=uid, is_active=True)
            # print user
            # print request.META
        except AppUser.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid session id')

        return (user, None)


class SessionAuthenticationAllMethods(authentication.BaseAuthentication):
    """
    A Session Id is expected for any kind of request.
    If a valid Session Id is not present, error will be raised.
    """
    def authenticate(self, request):
        session_id = getSessionId(request)
        sessionStore = SessionStore(session_key=session_id)
        uid = sessionStore.get('_auth_user_id', '')

        # Add the session object into request
        request.session = sessionStore

        if not uid:
            raise exceptions.AuthenticationFailed('Invalid session id')
        try:
            user = AppUser.objects.get(id=uid, is_active=True)
        except AppUser.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid session id')

        return (user, None)
