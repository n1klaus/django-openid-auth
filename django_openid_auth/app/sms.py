# Africastalking configuration
import json

import africastalking
from app.models import Customer
from django.conf import settings
from django.http import HttpResponse

africastalking.initialize(
    username=settings.AFRICASTALKING_USERNAME, api_key=settings.AFRICASTALKING_API_KEY
)


def notify_customer(request, data=None):
    try:
        if not data:
            data: dict = json.loads(request.body)
        message = data.get("message", settings.DEFAULT_SMS_MESSAGE)
        recipients = data.get("recipients")
        sms = africastalking.SMS
        response = sms.send(
            message=message,
            recipients=recipients,
            sender_id=settings.AFRICASTALKING_SENDER_ID,
        )
        json_response = json.dumps(response)
        return json_response
    except Exception:
        raise


def send_sms(request, data=None):
    if request.method == "POST":
        try:
            json_response = notify_customer(request, data)
            return HttpResponse(json_response, content_type="application/json")
        except Exception:
            raise
