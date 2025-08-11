from django.db import models
from django.core.validators import MinLengthValidator
from cloudinary.models import CloudinaryField
# Create your models here.


class Artist(models.Model):
    name = models.CharField(
        max_length=100, validators=[MinLengthValidator(1)], unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = CloudinaryField(
        'image', default='default-artist_fw2mea')
    debut_year = models.PositiveIntegerField(null=True, blank=True)
    bio = models.CharField(max_length=500, null=True, blank=True)
