from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from django.utils.decorators import method_decorator
from appauth.decorators import valid_ip_access

from django.views.generic import View

from django.contrib.auth import authenticate, login, logout


class LoginView(View):
    """
    A view for logging in a user.
    """
    template_name = 'appauth/login.html'

    @method_decorator(valid_ip_access)
    def get(self, request):
        context = {}
        return render(request, self.template_name, context)

    @method_decorator(valid_ip_access)
    def post(self, request):
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        if email and password:
            email = email.lower()
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                next_page = request.GET.get('next', None)
                if next_page:
                    return HttpResponseRedirect(next_page)
                return HttpResponseRedirect(reverse('home'))
            else:
                context = {'success': False, 'message': 'Incorrect email or password'}
        else:
            context = {'success': False, 'message': 'Email or password cannot be empty'}
        return render(request, self.template_name, context)


class LogoutView(View):
    """
    A view for logging out a user.
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('appauth:login'))
