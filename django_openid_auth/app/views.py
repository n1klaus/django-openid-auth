from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpRequest
from django.http import JsonResponse
from rest_framework import viewsets
from .models import Customer, Order
import app.serializers as serializers
from django.core.exceptions import PermissionDenied

class CustomersView(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = serializers.CustomerViewSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'options']

class OrdersView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderViewSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'options']

        
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