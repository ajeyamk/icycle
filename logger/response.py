import decimal
import json
from django.shortcuts import render as django_render

from rest_framework.response import Response as DrfResponse
from .utils import ObjectLogger


def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError


class Response(DrfResponse):
    """
    Wrapper around Django Rest Framework Response class. Can take one or a list of logs and logs the response.
    No overhead if no logs are passed.
    """
    def __init__(self, data, status=None, template_name=None, headers=None, content_type=None, logs=None):
        if logs:
            obj_logger = ObjectLogger()
            if not isinstance(logs, list):
                logs = [logs, ]
            for log in logs:
                log = obj_logger.log_response(
                    log,
                    data if isinstance(data, str) else json.dumps(data, default=decimal_default),
                    status=str(status),
                    headers=headers,
                    content_type=str(content_type))
                log.save()
        super(Response, self).__init__(
            data,
            status=status,
            template_name=template_name,
            headers=headers,
            content_type=content_type)


def render(request, template_name, context=None, content_type=None, status=None, using=None, logs=None):
    """
    Wrapper around Django render method. Can take one or a list of logs and logs the response.
    No overhead if no logs are passed.
    """
    if logs:
        obj_logger = ObjectLogger()
        if not isinstance(logs, list):
            logs = [logs, ]
        for log in logs:
            log = obj_logger.log_response(
                log,
                context,
                status=str(status),
                headers='',
                content_type=str(content_type))
            log.save()
    return django_render(
        request,
        template_name,
        context=context,
        content_type=content_type,
        status=status,
        using=using)
