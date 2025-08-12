from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from colorfield.fields import ColorField
# Create your models here.


class Artist(models.Model):
    name = models.CharField(
        max_length=100, validators=[MinLengthValidator(1)], unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = CloudinaryField(
        'image', default='default-artist_fw2mea')
    debut_year = models.PositiveIntegerField(null=True, blank=True)
    bio = models.CharField(max_length=500, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = ColorField(format='hex')
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.name
