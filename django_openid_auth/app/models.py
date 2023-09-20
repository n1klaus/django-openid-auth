from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils import timezone

class Customer(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField()
    password = models.CharField(max_length=128, null=True)
    first_name = models.CharField(max_length=60, null=True)
    last_name = models.CharField(max_length=60, null=True)

    def save(self, *args, **kwargs):
        # Hash the password before saving the model
        self.password = make_password(self.password)
        super(Customer, self).save(*args, **kwargs)

class Order(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    item = models.CharField(max_length=60)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
