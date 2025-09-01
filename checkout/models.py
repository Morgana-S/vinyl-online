import uuid
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class Order(models.Model):
    ORDER_STATUSES = [
        ('processing', 'Processing'),
        ('out for delivery', 'Out for Delivery'),
        ('delivered', 'Delivered')
    ]
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='orders',
        blank=True,
        null=True)
    status = models.CharField(
        max_length=25,
        choices=ORDER_STATUSES,
        default='processing')
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    postcode = models.CharField(max_length=20)
    phone_number = PhoneNumberField(region=None)
    subtotal_cost = models.DecimalField(max_digits=6, decimal_places=2)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2)
    grand_total_cost = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.uuid
