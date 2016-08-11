import traceback
import json

from errorlog.models import ErrorLog


class ErrorMiddleware(object):
    def process_exception(self, request, exception):
        # -- General info
        error_log = ErrorLog(
            exception_type=type(exception).__name__,
            exception_message=exception.message,
            stack_trace=traceback.format_exc())
        error_log.request_url = request.get_full_path()
        error_log.request_method = request.method
        error_log.get_data = json.dumps(request.GET)
        error_log.post_data = json.dumps(request.POST)
        error_log.request_body = request.body
        error_log.cookies = json.dumps(request.COOKIES)

        # --- Request meta info
        error_log.meta = ','.join('"%s": "%s"' % (k, str(v)) for k, v in request.META.items())
        error_log.meta = '{%s}' % error_log.meta
        error_log.meta = error_log.meta.replace('\\', '|')

        # --- User info
        if request.user.is_authenticated():
            error_log.user_id = request.user.id
            error_log.user_name = request.user.email

        # --- User agent info
        user_agent = request.user_agent
        # Browser
        error_log.request_browser = user_agent.browser
        # OS
        error_log.request_os = user_agent.os
        # Device
        error_log.request_device = user_agent.device
        # Device type
        error_log.is_mobile = user_agent.is_mobile
        error_log.is_tablet = user_agent.is_tablet
        error_log.is_touch_capable = user_agent.is_touch_capable
        error_log.is_pc = user_agent.is_pc
        error_log.is_bot = user_agent.is_bot

        # --- Save
        error_log.save()
        return None


def log_session_error(request, exception):
    # -- General info
    error_log = ErrorLog(
        exception_type=type(exception).__name__,
        exception_message=exception.detail,
        stack_trace=traceback.format_exc())
    error_log.request_url = request.get_full_path()
    error_log.request_method = request.method
    error_log.get_data = json.dumps(request.GET)
    error_log.post_data = json.dumps(request.POST)
    error_log.request_body = '{}'
    error_log.cookies = json.dumps(request.COOKIES)

    # --- Request meta info
    error_log.meta = ','.join('"%s": "%s"' % (k, str(v)) for k, v in request.META.items())
    error_log.meta = '{%s}' % error_log.meta
    error_log.meta = error_log.meta.replace('\\', '|')

    # --- User info
    if request.user.is_authenticated():
        error_log.user_id = request.user.id
        error_log.user_name = request.user.email

    # --- User agent info
    user_agent = request.user_agent
    # Browser
    error_log.request_browser = user_agent.browser
    # OS
    error_log.request_os = user_agent.os
    # Device
    error_log.request_device = user_agent.device
    # Device type
    error_log.is_mobile = user_agent.is_mobile
    error_log.is_tablet = user_agent.is_tablet
    error_log.is_touch_capable = user_agent.is_touch_capable
    error_log.is_pc = user_agent.is_pc
    error_log.is_bot = user_agent.is_bot

    # --- Save
    error_log.save()
    return None
