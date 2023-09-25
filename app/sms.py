# Africastalking configuration
import json

import africastalking
from django.conf import settings
from django.http import HttpResponse

from app.models import Customer

africastalking.initialize(
    username=settings.AFRICASTALKING_USERNAME, api_key=settings.AFRICASTALKING_API_KEY
)


def notify_customer(request, data=None):
    try:
        if not data:
            data: dict = json.loads(request.body)
        message = data.get("message", settings.DEFAULT_SMS_MESSAGE)
        recipients = data.get("recipients")
        if not isinstance(message, str) and isinstance(recipients, list):
            return HttpResponse(status=400)
        sms = africastalking.SMS
        response = sms.send(
            message=message,
            recipients=recipients,
            sender_id=settings.AFRICASTALKING_SENDER_ID,
        )
        json_response = json.dumps(response)
        return json_response
    except Exception:
        return HttpResponse(status=500)


def send_sms(request, data=None):
    if request.method == "POST":
        try:
            json_response = notify_customer(request, data)
            return HttpResponse(json_response, content_type="application/json")
        except Exception:
            return HttpResponse(status=405)
