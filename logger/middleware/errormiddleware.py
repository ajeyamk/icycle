import traceback
import json

from logger.utils import Logger


class ErrorMiddleware(object):
    _initial_http_body = None

    def process_request(self, request):
        # this requires because for some reasons there is no way to access request.body
        # in the 'process_response' method.
        self._initial_http_body = request.body

    def process_exception(self, request, exception):
        Logger.log_error(request, self._initial_http_body, exception)

        return None


# def log_session_error(request, exception):
#     # -- General info
#     log = Log(
#         exception_type=type(exception).__name__,
#         message=exception.detail,
#         stack_trace=traceback.format_exc())
#     log.request_url = request.get_full_path()
#     log.request_method = request.method
#     log.get_data = json.dumps(request.GET)
#     log.post_data = json.dumps(request.POST)
#     log.request_body = '{}'
#     log.cookies = json.dumps(request.COOKIES)

#     # --- Request meta info
#     log.meta = ','.join('"%s": "%s"' % (k, str(v)) for k, v in request.META.items())
#     log.meta = '{%s}' % log.meta
#     log.meta = log.meta.replace('\\', '|')

#     # --- User info
#     if request.user.is_authenticated():
#         log.user_id = request.user.id
#         log.user_name = request.user.email

#     # --- User agent info
#     user_agent = request.user_agent
#     # Browser
#     log.request_browser = user_agent.browser
#     # OS
#     log.request_os = user_agent.os
#     # Device
#     log.request_device = user_agent.device
#     # Device type
#     log.is_mobile = user_agent.is_mobile
#     log.is_tablet = user_agent.is_tablet
#     log.is_touch_capable = user_agent.is_touch_capable
#     log.is_pc = user_agent.is_pc
#     log.is_bot = user_agent.is_bot

#     # --- Save
#     log.save()
#     return None
