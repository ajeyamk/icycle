from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import (
    Log,
    RequestLog,
)
from .constants import Keys
from .utils import Logger
from .response import (
    render as logger_render,
)
from .utils import RequestLogger


class AllLogs(View):
    template_name = 'logger/all_logs.html'

    def get(self, request):
        page = request.GET.get(Keys.PAGE, 1)
        show = request.GET.get(Keys.SHOW, 10)

        logs = Log.objects.all().order_by('-created_on')

        # Check the url filter
        url = request.GET.get(Keys.URL, '')
        if url:
            logs = logs.filter(request_url__icontains=url)

        # Check the log level filter
        log_level = request.GET.get(Keys.LOG_LEVEL, Keys.ALL).upper()
        if log_level == Keys.ERROR:
            logs = logs.filter(log_level=Log.ERROR)
        elif log_level == Keys.DEBUG:
            logs = logs.filter(log_level=Log.DEBUG)
        elif log_level == Keys.WARN:
            logs = logs.filter(log_level=Log.WARN)
        elif log_level == Keys.INFO:
            logs = logs.filter(log_level=Log.INFO)

        # Check for the the request method
        method = request.GET.get(Keys.REQUEST_METHOD, '')
        if method:
            logs = logs.filter(request_method=method.upper())

        paginator = Paginator(logs, show)

        try:
            logs = paginator.page(page)
        except EmptyPage:
            logs = paginator.page(paginator.num_pages)

        query_string = '&show=%s&url=%s&level=%s&method=%s' % (
            show, url, log_level, method)

        context = {'logs': logs, 'log_levels': Log.LOG_LEVELS, 'query_string': query_string}
        return render(request, self.template_name, context)

    def post(self, request):
        Log.objects.all().delete()
        return HttpResponseRedirect(reverse('logger:all_logs'))


class AllRequestLogs(View):
    template_name = 'logger/all_request_logs.html'

    def get(self, request):
        page = request.GET.get('page', 1)
        show = request.GET.get(Keys.SHOW, 10)

        logs = RequestLog.objects.all().order_by('-created_on')

        # Check the url filter
        url = request.GET.get(Keys.URL, '')
        if url:
            logs = logs.filter(url__icontains=url)

        # Check for the the request method
        method = request.GET.get(Keys.REQUEST_METHOD, '')
        if method:
            logs = logs.filter(method=method.upper())

        # Check for the the request method
        status = request.GET.get(Keys.RESPONSE_STATUS, '')
        try:
            status = int(status)
        except Exception:
            status = None
        if status:
            logs = logs.filter(
                response_status__gte=status,
                response_status__lt=(status + 100))

        paginator = Paginator(logs, show)

        try:
            logs = paginator.page(page)
        except EmptyPage:
            logs = paginator.page(paginator.num_pages)

        query_string = '&show=%s&status=%s&url=%s&method=%s' % (
            show, status, url, method)

        context = {'logs': logs, 'query_string': query_string}
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
