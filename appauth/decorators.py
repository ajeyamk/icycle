from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse

from django.conf import settings


def validate_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    if ip:
        if ip in settings.ALLOWED_IPS:
            return True
        else:
            return False
    else:
        return False


def valid_ip_access(function):
    """
    A method decorator allowing only Admins to access a method.
    """
    def _arguments_wrapper(request, *args, **kwargs):
        # Validate IP
        if not validate_ip(request):
            return HttpResponse("Your IP is invalid!")
        return function(request, *args, **kwargs)

    _arguments_wrapper.__doc__ = function.__doc__
    _arguments_wrapper.__name__ = function.__name__
    return _arguments_wrapper


def ip_access(function):
    """
    A method decorator allowing only IPs listed in settings.ALLOWED_IPS
    """
    def _arguments_wrapper(request, *args, **kwargs):
        # Validate IP
        if not validate_ip(request):
            return HttpResponse("Your IP is invalid!")
        else:
            return function(request, *args, **kwargs)

    _arguments_wrapper.__doc__ = function.__doc__
    _arguments_wrapper.__name__ = function.__name__
    return _arguments_wrapper


def logged_in_access(function):
    """
    A method decorator allowing only Logged in users to access a method.
    """
    def _arguments_wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('http_403'))

    _arguments_wrapper.__doc__ = function.__doc__
    _arguments_wrapper.__name__ = function.__name__
    return _arguments_wrapper


def admin_access(function):
    """
    A method decorator allowing only Admins to access a method.
    """
    def _arguments_wrapper(request, *args, **kwargs):
        # Validate IP
        if not validate_ip(request):
            return HttpResponse("Your IP is invalid!")
        if request.user.is_anonymous():
            return HttpResponseRedirect(reverse('appauth:login'))
        try:
            if request.user.is_admin:
                return function(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('http_403'))
        except AttributeError:
            return HttpResponseRedirect(reverse('http_403'))

    _arguments_wrapper.__doc__ = function.__doc__
    _arguments_wrapper.__name__ = function.__name__
    return _arguments_wrapper


def access_to(roles):
    """
    A method decorator allowing only Admins or allowed roles to access a method.
    """
    def _method_wrapper(function):
        def _arguments_wrapper(request, *args, **kwargs):
            # Validate IP
            if not validate_ip(request):
                return HttpResponse("Your IP is invalid!")
            if request.user.is_anonymous():
                return HttpResponseRedirect(reverse('appauth:login'))
            try:
                user_roles = request.user.roles.all()
                user_roles = [role.role_name for role in user_roles]
                has_access = False
                for role in user_roles:
                    if role in roles:
                        has_access = True

                if request.user.is_admin or has_access:
                    return function(request, *args, **kwargs)
                else:
                    return HttpResponseRedirect(reverse('http_403'))
            except AttributeError:
                return HttpResponseRedirect(reverse('http_403'))
        return _arguments_wrapper
    return _method_wrapper
