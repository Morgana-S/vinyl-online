from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.text import slugify
from .models import Artist, Genre, Record, RecordImage, Review



class ArtistModelTest(TestCase):
    """
    TestCase for the Artist model.
    """
    def setUp(self):
        # Create some genres
        self.genre1 = Genre.objects.create(
            name='Rock', color='#ff0000', description='Rock music')
        self.genre2 = Genre.objects.create(
            name='Pop', color='#00ff00', description='Pop music')

        # Create an artist
        self.artist = Artist.objects.create(
            name='Test Artist',
            debut_year=2000,
            bio='A short bio'
        )

        # Create some records for the artist
        self.record1 = Record.objects.create(
            title='Record 1',
            artist=self.artist,
            size='12"',
            rpm='33',
            price=10.00,
            quantity=5
        )
        self.record1.genre.set([self.genre1])  # Set M2M field after creation

        self.record2 = Record.objects.create(
            title='Record 2',
            artist=self.artist,
            size='12"',
            rpm='33',
            price=15.00,
            quantity=2
        )
        self.record2.genre.set([self.genre2])

        self.record3 = Record.objects.create(
            title='Record 3',
            artist=self.artist,
            size='12"',
            rpm='33',
            price=20.00,
            quantity=1
        )
        # duplicate genre to test distinct
        self.record3.genre.set([self.genre1])

    # Tests whether the string represents the artist name
    def test_string_representation(self):
        self.assertEqual(str(self.artist), 'Test Artist')

    # Tests whether a slug is automatically created
    def test_slug_is_auto_created(self):
        self.assertEqual(self.artist.slug, slugify(self.artist.name))

    # Tests that genres only returns unique genres
    def test_genres_property_returns_distinct_genres(self):
        genres = self.artist.genres
        self.assertEqual(set(genres), {self.genre1, self.genre2})


class GenreModelTest(TestCase):
    """
    TestCase for the Genre model.
    """
    def setUp(self):
        self.genre = Genre.objects.create(
            name='Jazz',
            color='#123456',
            description='Smooth jazz music'
        )

    # Tests that the string represents the genre name
    def test_string_representation(self):
        self.assertEqual(str(self.genre), 'Jazz')

    # Tests that the slug is automatically created
    def test_slug_is_auto_created(self):
        self.assertEqual(self.genre.slug, slugify(self.genre.name))


class RecordModelTest(TestCase):
    """
    TestCase for the Record model.
    """
    def setUp(self):
        # Create artist and genres
        self.artist = Artist.objects.create(name='Test Artist')
        self.genre1 = Genre.objects.create(
            name='Rock', color='#ff0000', description='Rock music')
        self.genre2 = Genre.objects.create(
            name='Pop', color='#00ff00', description='Pop music')

        # Create a record
        self.record = Record.objects.create(
            title='Test Record',
            artist=self.artist,
            size='12"',
            rpm='33',
            price=12.50,
            quantity=5
        )
        self.record.genre.set([self.genre1, self.genre2])

        # Create a front cover image
        self.front_cover = RecordImage.objects.create(
            record=self.record,
            image_type='Front Cover'
        )

        # Create user for reviews
        self.user = User.objects.create_user(
            username='tester', password='testpass')

        # Create reviews
        Review.objects.create(
            author=self.user,
            record=self.record,
            delivery_rating=5,
            quality_rating=4,
            record_rating=3
        )
        Review.objects.create(
            author=self.user,
            record=self.record,
            delivery_rating=3,
            quality_rating=2,
            record_rating=4
        )

    # Tests that the string is the record's title
    def test_string_representation(self):
        self.assertEqual(str(self.record), 'Test Record')

    # Test that a slug can be automatically created
    def test_slug_is_auto_created(self):
        self.assertEqual(self.record.slug, slugify(self.record.title))

    # Tests whether the record is hidden if the quantity is 0
    def test_hidden_is_true_when_quantity_zero(self):
        self.record.quantity = 0
        self.record.save()
        self.assertTrue(self.record.hidden)

    # Tests that genres can be assigned
    def test_genres_assignment(self):
        self.assertEqual(set(self.record.genre.all()),
                         {self.genre1, self.genre2})

    # Tests that the front cover is called correctly
    def test_get_front_cover(self):
        cover = self.record.get_front_cover()
        self.assertEqual(cover, self.front_cover)

    # Tests that the average rating is correctly calculated
    def test_get_average_rating(self):
        avg_rating = self.record.get_average_rating()
        expected_avg = (3 + 4) / 2
        self.assertEqual(avg_rating, expected_avg)


class RecordImageModelTest(TestCase):
    """
    TestCase for the RecordImage model.
    """
    def setUp(self):
        # Create artist
        self.artist = Artist.objects.create(name='Test Artist')

        # Create a record
        self.record = Record.objects.create(
            title='Test Record',
            artist=self.artist,
            size='12"',
            rpm='33',
            price=12.50,
            quantity=5
        )

        # Create a record image
        self.image = RecordImage.objects.create(
            record=self.record,
            image_type='Front Cover'
        )

    # Tests that the string is correct
    def test_string_representation(self):
        expected_str = f'Front Cover image for {self.record}'
        self.assertEqual(str(self.image), expected_str)

    # Tests that the record relationship is set up
    def test_image_record_relationship(self):
        self.assertEqual(self.image.record, self.record)

    # Tests that image types are assigned correctly
    def test_image_type_assignment(self):
        self.assertEqual(self.image.image_type, 'Front Cover')


class ReviewModelTest(TestCase):
    """
    TestCase for the Review model.
    """
    def setUp(self):
        # Create artist and record
        self.artist = Artist.objects.create(name='Test Artist')
        self.record = Record.objects.create(
            title='Test Record',
            artist=self.artist,
            size='12"',
            rpm='33',
            price=12.50,
            quantity=5
        )

        # Create user
        self.user = User.objects.create_user(
            username='tester', password='testpass')

        # Create review
        self.review = Review.objects.create(
            author=self.user,
            record=self.record,
            delivery_rating=4,
            quality_rating=3,
            record_rating=5,
            store_feedback='Good store!',
            review_text='Loved it!'
        )

    # Tests that the user and record associations are correct
    def test_author_and_record_association(self):
        self.assertEqual(self.review.author, self.user)
        self.assertEqual(self.review.record, self.record)

    # Tests the record rating star conversion
    def test_record_rating_stars(self):
        stars_html = self.review.record_rating_stars
        # 5 filled stars and 0 empty
        self.assertIn('fa-solid fa-star', stars_html)
        self.assertNotIn('fa-regular fa-star', stars_html.replace(
            '<i class="fa-solid fa-star text-warning"></i>', ''))

    # Tests the delivery rating star conversion
    def test_delivery_rating_stars(self):
        stars_html = self.review.delivery_rating_stars
        # 4 filled stars and 1 empty
        self.assertIn(
            '<i class="fa-solid fa-star text-warning"></i>', stars_html)
        self.assertIn(
            '<i class="fa-regular fa-star text-warning"></i>', stars_html)

    # Tests the quality rating star conversion
    def test_quality_rating_stars(self):
        stars_html = self.review.quality_rating_stars
        # 3 filled stars and 2 empty
        filled_count = stars_html.count('fa-solid fa-star')
        empty_count = stars_html.count('fa-regular fa-star')
        self.assertEqual(filled_count, 3)
        self.assertEqual(empty_count, 2)

    # Test that store feedback and review text saves correctly
    def test_store_feedback_and_review_text(self):
        self.assertEqual(self.review.store_feedback, 'Good store!')
        self.assertEqual(self.review.review_text, 'Loved it!')
