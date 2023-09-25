from rest_framework import serializers

from .models import Customer
from .models import Order


class CustomerViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ["created_at", "updated_at"]

    def create(self, validated_data):
        # Implement any necessary data sanitization before creating the object
        # Example: sanitize user input to prevent SQL injection or XSS attacks
        validated_data["first_name"] = validated_data["first_name"].strip()
        validated_data["last_name"] = validated_data["last_name"].strip()
        # Add more sanitization steps as needed
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Implement any necessary data sanitization before updating the object
        # Example: sanitize user input to prevent SQL injection or XSS attacks
        if validated_data.get("first_name"):
            validated_data["first_name"] = validated_data["first_name"].strip()
        if validated_data.get("last_name"):
            validated_data["last_name"] = validated_data["last_name"].strip()
        if validated_data.get("email"):
            validated_data["email"] = validated_data["email"].strip()
        if validated_data.get("password"):
            validated_data["password"] = validated_data["password"].strip()
        # Add more sanitization steps as needed
        return super().update(instance, validated_data)


class OrderViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ["created_at", "updated_at"]

    def create(self, validated_data):
        # Implement any necessary data sanitization before creating the object
        # Example: sanitize user input to prevent SQL injection or XSS attacks
        validated_data["item"] = validated_data["item"].strip()
        # Add more sanitization steps as needed
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Implement any necessary data sanitization before updating the object
        # Example: sanitize user input to prevent SQL injection or XSS attacks
        if validated_data.get("item"):
            validated_data["item"] = validated_data["item"].strip()
        # Add more sanitization steps as needed
        return super().update(instance, validated_data)
