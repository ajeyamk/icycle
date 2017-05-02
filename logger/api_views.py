from rest_framework.views import APIView
from rest_framework import status

from .response import (
    Response as LoggerResponse,
)

from .utils import Logger


class TestAPILogs(APIView):

    def get(self, request):
        logs = [
            Logger.log_warn(request)]
        return LoggerResponse(
            {'foo': 'bar'},
            status=status.HTTP_400_BAD_REQUEST,
            logs=logs)
