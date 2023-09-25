# Create your tests here.
import json
from unittest.mock import patch

from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.test import Client
from django.test import RequestFactory
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Customer
from .models import Order
from .serializers import CustomerViewSerializer
from .serializers import OrderViewSerializer
from app.openid import MyOpenIdConnectBackend
from app.sms import notify_customer
from app.sms import send_sms


class BaseModelTestCase(TestCase):
    def check_timestamps(self, instance):
        # Positive test case: Ensure that the created_at and updated_at fields are set correctly
        self.assertIsNotNone(instance.created_at)
        self.assertIsNotNone(instance.updated_at)


class CustomerModelTestCase(BaseModelTestCase):
    def setUp(self):
        self.test_password = "Password!23"
        customer_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": self.test_password,
        }
        self.customer = Customer.objects.create(**customer_data)

    def test_password_hashing(self):
        # Positive test case: Ensure that the password is hashed correctly
        self.assertTrue(check_password(self.test_password, self.customer.password))
        # Negative test case: Ensure that the password is not stored in plain text
        self.assertNotEqual(self.test_password, self.customer.password)

    def test_save_instance(self):
        self.check_timestamps(self.customer)


class OrderModelTestCase(BaseModelTestCase):
    def setUp(self):
        customer_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "Password!23",
        }
        self.customer = Customer.objects.create(**customer_data)
        order_data = {"item": "Test Item", "amount": "10", "customer_id": self.customer}
        self.order = Order.objects.create(**order_data)

    def test_customer_foreign_key(self):
        # Positive test case: Ensure that the customer_id foreign key is set correctly
        self.assertEqual(self.order.customer_id, self.customer)

        # Negative test case: Ensure that the customer_id foreign key cannot be null
        with self.assertRaises(Exception):
            Order.objects.create(item="Test Item", amount="10.0")

    def test_save_instance(self):
        self.check_timestamps(self.order)


class SerializerTestCase(TestCase):
    def check_valid_data(self, serializer, data):
        serializer_instance = serializer(data=data)
        self.assertTrue(serializer_instance.is_valid())
        self.assertEqual(serializer_instance.errors, {})

    def check_missing_fields(self, serializer, data, errors):
        serializer_instance = serializer(data=data)
        self.assertFalse(serializer_instance.is_valid())
        self.assertEqual(serializer_instance.errors, errors)


class CustomerViewSerializerTest(SerializerTestCase):
    def test_valid_data(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "Password!23",
        }
        self.check_valid_data(CustomerViewSerializer, data)

    def test_missing_fields(self):
        data = {
            "first_name": "John",
            "last_name": "",
            "email": "john.doe@example.com",
            "password": "",
        }
        errors = {
            "last_name": ["Last Name cannot be empty."],
            "password": ["Password cannot be empty."],
        }
        self.check_missing_fields(CustomerViewSerializer, data, errors)


class OrderViewSerializerTest(SerializerTestCase):
    def test_valid_data(self):
        data = {"item": "Test Product", "amount": "10", "customer_id": 1}
        self.check_valid_data(OrderViewSerializer, data)

    def test_missing_fields(self):
        data = {"item": "", "amount": None, "customer_id": 1}
        errors = {
            "item": ["Item cannot be empty."],
            "amount": ["Amount cannot be empty."],
        }
        self.check_missing_fields(OrderViewSerializer, data, errors)


class CustomersViewTestCase(TestCase):
    def setUp(self):
        customer_data = {
            "first_name": "Gal",
            "last_name": "Gadot",
            "email": "galgadot@email.com",
            "password": "Password8!!",
        }
        self.client = APIClient()
        self.customer = Customer.objects.create(**customer_data)

    def test_get_all_customers(self):
        response = self.client.get("/customers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["email"], "galgadot@email.com")

    def test_get_one_customer(self):
        response = self.client.get("/customers/1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data["email"], "galgadot@email.com")

    def test_create_customer(self):
        data = {
            "first_name": "Charlize",
            "last_name": "Theron",
            "email": "charlizetheron@example.com",
            "password": "Password8??",
        }
        response = self.client.post("/customers/", data=data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)
        self.assertEqual(response.data["email"], "charlizetheron@example.com")

    def test_update_customer(self):
        data = {"first_name": "Angelina", "last_name": "Jolie"}
        response = self.client.put(f"/customers/{self.customer.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Angelina")
        self.assertEqual(response.data["last_name"], "Jolie")

    def test_delete_customer(self):
        response = self.client.delete(f"/customers/{self.customer.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Customer.objects.count(), 0)


class OrdersViewTestCase(TestCase):
    def setUp(self):
        customer_data = {
            "first_name": "Ronoroa",
            "last_name": "Zoro",
            "email": "ronoroazoro@email.com",
            "password": "Password8&&",
        }
        self.client = APIClient()
        self.customer = Customer.objects.create(**customer_data)
        self.order = Order.objects.create(
            customer_id=self.customer, amount="100", item="Shinai"
        )

    def test_get_all_orders(self):
        response = self.client.get("/orders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["item"], "Shinai")

    def test_get_one_order(self):
        response = self.client.get(f"/orders/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data["item"], "Shinai")

    def test_create_order(self):
        data = {
            "customer_id": self.customer.id,
            "amount": "1000",
            "item": "Katana Sword",
        }
        response = self.client.post("/orders/", data=data)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(response.data["item"], "Katana Sword")

    def test_update_order(self):
        data = {"total_amount": "1500"}
        response = self.client.put(f"/orders/{self.order.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["amount"], "1500")

    def test_delete_order(self):
        response = self.client.delete(f"/orders/{self.order.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)


class CustomerOrdersViewTestCase(TestCase):
    def setUp(self):
        customer_data = {
            "first_name": "Tony",
            "last_name": "Jaa",
            "email": "tonyjaa@email.com",
            "password": "Password8%%",
        }
        self.client = APIClient()
        self.customer = Customer.objects.create(**customer_data)
        self.order = Order.objects.create(
            customer_id=self.customer, amount="100", item="Nunchakus"
        )

    def test_get_customer_orders(self):
        url = reverse("customer-orders", args=[self.customer.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["customer_id"], self.customer.id)
        self.assertEqual(response.data[0]["item"], "Nunchakus")

    def test_get_customer_orders_invalid_customer_id(self):
        response = self.client.get(reverse("customer-orders", args=[999]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
