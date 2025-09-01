import uuid
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from records.models import Record
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
        return f'{self.uuid} | Total: {self.grand_total_cost}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE, related_name='items')
    record = models.ForeignKey(
        Record,
        null=False,
        blank=False)
    quantity = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(9),
        ]
    )
    item_total = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        blank=False,
        editable=False
    )

    def __str__(self):
        return f'({self.record.name} x {self.quantity} - {self.item_total})'

    def save(self, *args, **kwargs):
        self.item_total = self.record.price * self.quantity
        super().save(*args, *kwargs)
