from django.contrib import admin

from .models import ErrorLog


class ErrorLogAdmin(admin.ModelAdmin):
    readonly_fields = ['request_url', 'request_method', 'get_data', 'post_data', 'cookies', 'meta',
        'exception_type', 'exception_message', 'stack_trace', 'user_id', 'user_name', 'created_on']

    def has_add_permission(self, request):
        return False


admin.site.register(ErrorLog, ErrorLogAdmin)
