from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'global/home.html', {})


def health(request):
    return HttpResponse("Server seems to be working fine")
