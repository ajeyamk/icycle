from django.shortcuts import render
from django.views.generic import View

from django.http import HttpResponse


class IndexView(View):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name, {})


def health(request):
    return HttpResponse('Seems to be working fine')
