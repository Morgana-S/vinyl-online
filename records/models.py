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


class Record(models.Model):
    RECORD_SIZES = [('7"', '7 Inch'), ('10"', '10 Inch'), ('12"', '12 Inch')]
    RECORD_RPM = [('33', '33RPM'), ('45', '45RPM'), ('78', '78RPM')]
    title = models.CharField(
        max_length=100, validators=[MinLengthValidator(1)])
    slug = models.SlugField(max_length=100, unique=True)
    artist = models.ForeignKey(
        Artist, on_delete=models.PROTECT, related_name='records_by_artist')
    release_date = models.DateField(blank=True, null=True)
    genre = models.ManyToManyField(
        Genre, blank=True, related_name='records_by_genre')
    size = models.CharField(max_length=10, choices=RECORD_SIZES)
    rpm = models.CharField(max_length=10, choices=RECORD_RPM)
    description = models.CharField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class RecordImage(models.Model):
    IMAGE_TYPES = [
        ('Front Cover', 'Front Cover'),
        ('Back Cover', 'Back Cover'),
        ('Disk', 'Disk'),
        ('Insert/Leaflet', 'Insert/Leaflet'),
        ('Other', 'Other'),
        ]
    record = models.ForeignKey(
        Record, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField(
        'image', default='default-record_rjj3wh')
    image_type = models.CharField(
        max_length=50, choices=IMAGE_TYPES, default='Front Cover')
