import logging
import os
import requests

from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from mocrat_user.models import User
from mocrat_config.environ_config import env
from mocrat_config.admin_utils import error_notify


logger = logging.getLogger(__name__)

class PostText(APIView):
    def post(self, request):
        logger.info("Called mocrat_discord PostText")

        webhook_url = request.data["discord_webhook_url"]
        text = request.data["text"]
        payload = {
            "content": text
        }
        response = requests.post(webhook_url, json=payload)
        logger.info("Status {}, webhook_url : {}, content : {}".format(response, webhook_url, text))

        return Response(status=None)