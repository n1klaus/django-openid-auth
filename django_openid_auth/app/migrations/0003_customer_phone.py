# Generated by Django 4.2.5 on 2023-09-20 11:26
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0002_rename_customer_id_order_customer"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="phone",
            field=models.CharField(max_length=20, null=True),
        ),
    ]
