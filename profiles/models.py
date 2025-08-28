import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from allauth.account.models import EmailAddress
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class UserProfile(models.Model):
    UUID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(
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
