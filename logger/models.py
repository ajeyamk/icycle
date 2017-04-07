from __future__ import unicode_literals

from django.db import models


class Log(models.Model):
    ERROR = 1
    DEBUG = 2
    WARN = 3
    INFO = 4
    LOG_LEVELS = (
        (ERROR, 'ERROR'),
        (DEBUG, 'DEBUG'),
        (WARN, 'WARN'),
        (INFO, 'INFO'),
    )

    log_level = models.IntegerField(
        choices=LOG_LEVELS,
        default=4)
    request_url = models.CharField(
        max_length=2083,
        blank=True)
    request_method = models.CharField(
        max_length=10,
        blank=True)
    get_data = models.TextField(
        blank=True)
    request_body = models.TextField(
        blank=True)
    cookies = models.TextField(
        blank=True)
    meta = models.TextField(
        blank=True)
    exception_type = models.CharField(
        max_length=2083,
        blank=True)
    message = models.TextField(
        blank=True)
    stack_trace = models.TextField(
        blank=True)
    user_id = models.IntegerField(
        blank=True,
        null=True)
    user_name = models.CharField(
        max_length=255,
        blank=True)
    request_browser = models.CharField(
        max_length=255,
        blank=True)
    request_os = models.CharField(
        max_length=255,
        blank=True)
    request_device = models.CharField(
        max_length=255,
        blank=True)
    response_body = models.TextField(
        blank=True)
    response_status = models.CharField(
        max_length=255,
        blank=True)
    response_headers = models.TextField(
        blank=True)
    response_content_type = models.CharField(
        max_length=255,
        blank=True)
    is_mobile = models.BooleanField(
        default=False)
    is_tablet = models.BooleanField(
        default=False)
    is_touch_capable = models.BooleanField(
        default=False)
    is_pc = models.BooleanField(
        default=False)
    is_bot = models.BooleanField(
        default=False)
    created_on = models.DateTimeField(
        auto_now_add=True)

    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"

    def __unicode__(self):
        return self.exception_type


class RequestLog(models.Model):
    # GET = 1
    # POST = 2
    # PUT = 3
    # DELETE = 4
    # OPTIONS = 5
    # PATCH = 6
    # HEAD = 7
    # METHODS = (
    #     (GET, 'GET'),
    #     (POST, 'POST'),
    #     (PUT, 'PUT'),
    #     (DELETE, 'DELETE'),
    #     (OPTIONS, 'OPTIONS'),
    #     (PATCH, 'PATCH'),
    #     (HEAD, 'HEAD'),
    # )

    method = models.CharField(
        max_length=10,
        blank=True)
    url = models.CharField(
        max_length=2043,
        blank=True)
    request_data = models.TextField(
        blank=True)
    request_headers = models.TextField(
        blank=True)
    response_text = models.TextField(
        blank=True)
    response_status = models.IntegerField(
        null=True)
    response_reason = models.CharField(
        max_length=255,
        blank=True)
    response_time = models.IntegerField(
        blank=True)
    user_id = models.IntegerField(
        blank=True,
        null=True)
    user_name = models.CharField(
        max_length=255,
        blank=True)
    created_on = models.DateTimeField(
        auto_now_add=True)
    message = models.TextField(
        blank=True)

    class Meta:
        verbose_name = "Request Log"
        verbose_name_plural = "Request Logs"

    def __unicode__(self):
        return '%s %s' % (self.method, self.url)
