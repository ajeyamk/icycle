from django.contrib.sessions.backends.db import SessionStore
from .models import AppUser

from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.permissions import SAFE_METHODS
import hashlib, base64, hmac, json
from django.conf import settings

from django.conf import settings


def getSessionId(request):
    session_id = request.COOKIES.get('sessionid', '')
    if not session_id:
        session_id = request.META.get('HTTP_SESSIONID', '')
        if not session_id:
            raise exceptions.AuthenticationFailed('Invalid session id')
    return session_id


def getToken(request):
    token = request.COOKIES.get('token', '')
    if not token:
        token = request.META.get('HTTP_TOKEN', '')
        if not token:
            raise exceptions.AuthenticationFailed('Token missing')
    return token


class TokenAuthenticationUnsafeMethods(authentication.BaseAuthentication):
    """
    Just a token is expected only for UNSAFE methods, i.e: PUT, POST, DELETE
    SAFE_METHODS get free passage and token is not checked.
    """
    def authenticate(self, request):
        if request.method in SAFE_METHODS:
            return (None, None)

        token = getToken(request)
        if token == settings.API_TOKEN:
            return (None, None)
        else:
            raise exceptions.AuthenticationFailed('Invalid token')


class TokenAuthenticationAllMethods(authentication.BaseAuthentication):
    """
    Just a token is expected only for UNSAFE methods, i.e: PUT, POST, DELETE
    SAFE_METHODS get free passage and token is not checked.
    """
    def authenticate(self, request):
        token = getToken(request)
        if token == settings.API_TOKEN:
            return (None, None)
        else:
            raise exceptions.AuthenticationFailed('Invalid token')


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


class AdminAuthenticationAllMethods(authentication.BaseAuthentication):
    """
    A Session Id is expected for any kind of request.
    If a valid Session Id is not present or if the user is not admin, error will be raised.
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
        if not user.is_admin:
            raise exceptions.AuthenticationFailed('User is not an admin')

        return (user, None)


class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    """
    Do not check for CSRF token
    """
    def enforce_csrf(self, request):
        return


def _hmac_is_valid(body, secret, hmac_to_verify):
    hash = hmac.new(secret, body, hashlib.sha256)
    hmac_calculated = base64.b64encode(hash.digest())
    return hmac_calculated == hmac_to_verify


class AuthenticateWebHook(authentication.BaseAuthentication):

    def authenticate(self, request):
        try:
            webhook_topic = request.META['HTTP_X_SHOPIFY_TOPIC']
            webhook_hmac = request.META['HTTP_X_SHOPIFY_HMAC_SHA256']
            webhook_data = json.loads(request.body)
        except:
            raise exceptions.AuthenticationFailed('Shopify Secret key is mandatory')
        # Verify the HMAC.
        if not _hmac_is_valid(request.body, settings.SHOPIFY_API_SECRET, webhook_hmac):
            raise exceptions.AuthenticationFailed('Shopify integrity check failed')
        else:
            request.webhook_topic = webhook_topic
            request.webhook_data = webhook_data
            pass
