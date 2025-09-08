from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum
from phonenumber_field.modelfields import PhoneNumberField
from records.models import Record
import uuid
# Create your models here.


class Order(models.Model):
    """
    Represents an Order in the store.

    Each Order has a unique id PK (for obscurification but also to allow
    anonymous users to view their order confirmation on the site), optional
    user, status, full_name, address_line1, address_line2, city, postcode,
    phone_number, email, subtotal_cost, delivery_cost, grand_total_cost,
    created_at, and stripe_pid.

    Delivery and contact info is populated from the user's UserProfile and
    selected DeliveryAddress, if logged in.

    Functions:
    update_total - Updates the totals each time a line item is added or
    changed. Uses the signals.py file to recognize when this happens
    in the user's basket.
    """
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
    full_name = models.CharField(max_length=50)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    postcode = models.CharField(max_length=20)
    phone_number = PhoneNumberField(region=None)
    email = models.EmailField()
    subtotal_cost = models.DecimalField(max_digits=6, decimal_places=2)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2)
    grand_total_cost = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    stripe_pid = models.CharField(editable=False)

    def __str__(self):
        return f'{self.uuid} | Total: {self.grand_total_cost}'

    def update_total(self):
        """
        Updates the total each time a line item is added.
        """
        self.subtotal_cost = self.items.aggregate(Sum('item_total'))[
            'item_total__sum'] or 0
        if self.subtotal_cost < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = (self.subtotal_cost *
                                  Decimal(settings.STANDARD_DELIVERY_MODIFIER))
        else:
            self.delivery_cost = 0

        self.grand_total_cost = self.subtotal_cost + self.delivery_cost
        self.save()


class OrderItem(models.Model):
    """
    Represents a line item in the user's order.

    Each OrderItem has an order, record, quantity, and item_total.
    """
    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE, related_name='items')
    record = models.ForeignKey(
        Record,
        null=False,
        blank=False,
        on_delete=models.CASCADE)
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
        return (
            f'{self.record.title} x {self.quantity} - Order: {self.order.uuid}'
        )

    def save(self, *args, **kwargs):
        self.item_total = self.record.price * self.quantity
        super().save(*args, **kwargs)
