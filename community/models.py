import uuid
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class SupportTicket(models.Model):
    SUPPORT_CATEGORIES = [
        ('payment', 'Payment Issue'),
        ('delivery', 'Delivery Issue'),
        ('record', 'Record Quality or Condition Issue'),
        ('feedback', 'Feedback & Complaints'),
        ('other', 'Other'),
    ]

    STATUS_CATEGORIES = [
        ('open', 'Open'),
        ('closed', 'Resolved'),
    ]

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='support_tickets',
        blank=True, null=True,
    )
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    category = models.CharField(
        max_length=50, choices=SUPPORT_CATEGORIES, default='payment')
    description = models.TextField(
        help_text='Please let us know how we can help you.')
    status = models.CharField(
        max_length=10, choices=STATUS_CATEGORIES, default='open')


class NewsletterSubscriber(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='newsletter',
        blank=True,
    )
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
