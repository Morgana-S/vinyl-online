from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import uuid
# Create your models here.


class UserProfile(models.Model):
    """
    Represents a user's personal information in their profile.

    Each UserProfile has a user, first_name, last_nmae, contact_phone_number,
    and contact_email. Checkout forms will automatically prepopulate with this
    information if it exists.

    Functions:
    full_name - converts first + last names to a full_name for use in the
    checkout form.
    """
    UUID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(
        max_length=20, validators=[MinLengthValidator(1)])
    last_name = models.CharField(
        max_length=20, validators=[MinLengthValidator(1)])

    contact_phone_number = PhoneNumberField(region=None)

    contact_email = models.EmailField(
        help_text='If this is the same as the email you made the account with'
        ', you can leave this blank.', blank=True)

    def save(self, *args, **kwargs):
        if not self.contact_email:
            self.contact_email = self.user.email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    def full_name(self):
        return self.first_name + ' ' + self.last_name


class DeliveryAddress(models.Model):
    """
    Represents an instance of a user's delivery address.

    Each DeliveryAddress has a user, label, address_line1, address_line2,
    city, and postcode. address_line2 and city are optional.
    """
    UUID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='delivery_addresses'
    )
    label = models.CharField(
        blank=True, max_length=30, help_text=(
            'A useful label to describe what this address is, '
            'e.g. "Home", "Work"')
    )
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    postcode = models.CharField(max_length=20)

    def __str__(self):
        return self.label
