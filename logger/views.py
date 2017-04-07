from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import (
    Log,
    RequestLog,
)
from .utils import Logger
from .response import render as logger_render
from .utils import RequestLogger


class AllLogs(View):
    template_name = 'logger/all_logs.html'

    def get(self, request):
        page = request.GET.get('page', 1)

        logs = Log.objects.all().order_by('-created_on')
        paginator = Paginator(logs, 10)

        try:
            logs = paginator.page(page)
        except EmptyPage:
            logs = paginator.page(paginator.num_pages)

        context = {'logs': logs}
        return render(request, self.template_name, context)

    def post(self, request):
        Log.objects.all().delete()
        return HttpResponseRedirect(reverse('logger:all_logs'))


class AllRequestLogs(View):
    template_name = 'logger/all_request_logs.html'

    def get(self, request):
        page = request.GET.get('page', 1)

        logs = RequestLog.objects.all().order_by('-created_on')
        paginator = Paginator(logs, 10)

        try:
            logs = paginator.page(page)
        except EmptyPage:
            logs = paginator.page(paginator.num_pages)

        context = {'logs': logs}
        return render(request, self.template_name, context)

    def post(self, request):
        RequestLog.objects.all().delete()
        return HttpResponseRedirect(reverse('logger:all_request_logs'))


class TestLogs(View):
    template_name = 'logger/logger_test.html'

    def get(self, request):
        logs = [
            Logger.log_info(request, 'Some info message. For Django render.'),
            Logger.log_debug(request, 'Some debug message. For Django render.'),
            Logger.log_warn(request, 'Some warn message. For Django render.'),
        ]

        context = {'some': 'data'}
        return logger_render(request, self.template_name, context, logs=logs)


class TestRequestLogs(View):
    template_name = 'logger/logger_test.html'

    def get(self, request):
        response = RequestLogger.get(
            'https://jsonplaceholder.typicode.com/posts/1',
            params={'query': 'value'},
            user=request.user,
            message='Some post request message')
        return render(request, self.template_name, {'text': response.text})
