from django.contrib.auth.models import User
from django.db import models
import uuid
# Create your models here.


class SupportTicket(models.Model):
    """
    Represents a Support Ticket.

    Each Support Ticket has a user (optional), name, email, category,
    description, status, and created_at.

    Support tickets mostly exist as database objects to be accessed in the
    admin panel; the admin panel provides good functionality for site admins
    to address user problems.
    """
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
    created_at = models.DateTimeField(auto_now_add=True)


class NewsletterSubscriber(models.Model):
    """
    Represents a Newsletter Subscriber.

    Each NewsletterSubscriber can have an optional user, name, and email.
    These can then be called when sending out newsletters if a full
    newsletter is implemented.
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='newsletter',
        blank=True, null=True
    )
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
