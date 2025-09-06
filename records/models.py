from cloudinary.models import CloudinaryField
from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django.core.validators import (MinLengthValidator,
                                    MinValueValidator, MaxValueValidator)
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.text import slugify


# Create your models here.


class Artist(models.Model):
    name = models.CharField(
        max_length=100, validators=[MinLengthValidator(1)], unique=True)
    slug = models.SlugField(max_length=100,
                            unique=True,
                            blank=True,
                            help_text='This will be created automatically if '
                            'left blank.')
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

    @property
    def genres(self):
        """
        Looks through all of the artist's records and returns their distinct
        genres.
        """
        return Genre.objects.filter(records_by_genre__artist=self).distinct()


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(blank=True, unique=True)
    color = ColorField(format='hex')
    description = models.TextField(max_length=1000)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Record(models.Model):
    RECORD_SIZES = [('7"', '7 Inch'), ('10"', '10 Inch'), ('12"', '12 Inch')]
    RECORD_RPM = [('33', '33RPM'), ('45', '45RPM'), ('78', '78RPM')]
    title = models.CharField(
        max_length=100, validators=[MinLengthValidator(1)])
    slug = models.SlugField(max_length=100, unique=True, blank=True,
                            help_text='Slug will automatically generate if '
                            'left blank.')
    artist = models.ForeignKey(
        Artist, on_delete=models.PROTECT, related_name='records_by_artist')
    release_year = models.PositiveSmallIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1900), MaxValueValidator(2100)])
    genre = models.ManyToManyField(
        Genre, blank=True, related_name='records_by_genre')
    size = models.CharField(max_length=10, choices=RECORD_SIZES)
    rpm = models.CharField(max_length=10, choices=RECORD_RPM)
    description = models.CharField(max_length=5000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField()
    hidden = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.quantity == 0:
            self.hidden = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_front_cover(self):
        return self.images.filter(image_type="Front Cover").first()

    def get_average_rating(self):
        reviews = self.record_reviews.all()
        ratings = []
        for review in reviews:
            ratings.append(review.record_rating)

        average_rating = sum(ratings) / len(ratings)
        return average_rating


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

    def __str__(self):
        return f'{self.image_type} image for {self.record}'


class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    record = models.ForeignKey(
        Record,
        on_delete=models.CASCADE,
        related_name='record_reviews'
    )
    delivery_rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        help_text=('Rate the delivery from 1-5, with 5 being perfect.')
    )
    quality_rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        help_text=('Rate the quality of the record condition from 1-5, with '
                   '5 being perfect.')
    )
    record_rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        help_text='Rate how much you enjoyed the record, from 1-5.'
    )
    store_feedback = models.TextField(
        blank=True,
        help_text=(
            'Feel free to add any additional feedback about your '
            'purchase here.'
        ))
    review_text = models.TextField(
        blank=True,
        help_text=(
            'Feel free to describe your thoughts on the record here.'
        )
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    @property
    def record_rating_stars(self):
        """
        Render record_rating as star icons.
        """
        stars_html = ''.join(
            '<i class="fa-solid fa-star text-warning"></i>'
            for i in range(self.record_rating)
        )
        stars_html += ''.join(
            '<i class="fa-regular fa-star text-warning"></i>'
            for i in range(5 - self.record_rating)
        )

        return mark_safe(stars_html)

    @property
    def delivery_rating_stars(self):
        """
        Render delivery_rating as star icons.
        """
        stars_html = ''.join(
            '<i class="fa-solid fa-star text-warning"></i>'
            for i in range(self.delivery_rating)
        )
        stars_html += ''.join(
            '<i class="fa-regular fa-star text-warning"></i>'
            for i in range(5 - self.delivery_rating)
        )

        return mark_safe(stars_html)

    @property
    def quality_rating_stars(self):
        """
        Render quality_rating as star icons.
        """
        stars_html = ''.join(
            '<i class="fa-solid fa-star text-warning"></i>'
            for i in range(self.quality_rating)
        )
        stars_html += ''.join(
            '<i class="fa-regular fa-star text-warning"></i>'
            for i in range(5 - self.quality_rating)
        )

        return mark_safe(stars_html)
