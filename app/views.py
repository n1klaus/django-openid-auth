import json

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework import viewsets

import app.serializers as serializers
from .models import Customer
from .models import Order
from app.sms import notify_customer


class CustomersView(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = serializers.CustomerViewSerializer
    http_method_names = ["get", "post", "put", "patch", "delete", "options"]


class OrdersView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderViewSerializer
    http_method_names = ["get", "post", "put", "patch", "delete", "options"]

    def create(self, request, *args, **kwargs):
        try:
            # Retrieve the customer_id from the request body
            customer_id = request.data.get("customer")
            # Retrieve the customer object using the customer_id
            customer = Customer.objects.get(id=customer_id)
            # Create a new order object
            order = Order.objects.create(
                customer=customer,
                amount=request.data.get("amount"),
                item=request.data.get("item"),
            )
            # Send sms to the customer
            if not customer.phone:
                raise PermissionDenied("Phone number not found!")
            recipients = [customer.phone]
            sms_data = {
                "message": settings.DEFAULT_SMS_MESSAGE,
                "recipients": recipients,
            }
            notify_customer(request, sms_data)
            # Return the order object as a JSON response
            return JsonResponse(serializers.OrderViewSerializer(order).data, safe=False)

            # return super().create(request, *args, **kwargs)
        except Customer.DoesNotExist:
            raise PermissionDenied("Invalid customer_id")


class CustomerOrdersView(View):
    def get(self, request: HttpRequest, customer_id: int):
        try:
            # Retrieve the customer's orders using the customer_id parameter
            orders = Order.objects.filter(customer_id=customer_id)
            # Convert the QuerySet into a list of dictionaries
            orders_data = list(orders.values())
            # Return the orders_data as a JSON response
            return JsonResponse(orders_data, safe=False)
        except Order.DoesNotExist:
            raise PermissionDenied("Invalid customer_id")
