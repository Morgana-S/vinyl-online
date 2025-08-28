from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from allauth.account.models import EmailAddress
# Create your models here.


class UserProfile(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(
        max_length=20, validators=[MinLengthValidator(1)])
    last_name = models.CharField(
        max_length=20, validators=[MinLengthValidator(1)])

    def __str__(self):
        return self.user.username

    def full_name(self):
        return self.first_name + ' ' + self.last_name

    @property
    def contact_email(self):
        # Obtains the user's contact email from their primary email via allauth
        try:
            return EmailAddress.objects.get(user=self.user, primary=True.email)
        except EmailAddress.DoesNotExist:
            return self.user.email
