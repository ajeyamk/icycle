from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from appauth.api_authentications import (
    CsrfExemptSessionAuthentication,
)

from main.celery import get_celery_worker_status


class PingCelery(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, )

    def post(self, request):
        """
        Pings celery to check if it is available.
        """
        data = get_celery_worker_status()
        try:
            error = data["ERROR"]
            return Response(
                data,
                status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception:
            return Response(
                data,
                status=status.HTTP_200_OK)
