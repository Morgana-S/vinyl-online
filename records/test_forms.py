from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from unittest.mock import patch
from records.forms import RecordForm, ArtistForm
from records.models import Record, Artist, Genre


def get_test_image_file():
    # Minimal valid JPEG file
    img_data = (
        b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00'
        b'\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\x09'
        b'\x09\x08\n\x0c\x14\x0c\n\n\x0b\x0b\n'
        b'\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x03\x01"\x00\x02\x11\x01\x03\x11\x01'
        b'\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00?\x00\xd2\xcf \xff\xd9'
    )
    return SimpleUploadedFile("test.jpg", img_data, content_type="image/jpeg")


class RecordFormTest(TestCase):
    """
    TestCase for the RecordForm.
    """

    def setUp(self):
        self.artist = Artist.objects.create(name='Test Artist')
        self.genre1 = Genre.objects.create(name='Rock')
        self.genre2 = Genre.objects.create(name='Pop')

        self.valid_data = {
            'title': 'Test Album',
            'slug': 'test-album',
            'artist': self.artist.pk,
            'release_year': 2025,
            'genre': [self.genre1.pk, self.genre2.pk],
            'size': '12"',
            'rpm': 33,
            'description': 'Test description',
            'price': '15.99',
            'quantity': 5,
            'hidden': False
        }

    # Test form is valid
    def test_form_valid_with_valid_data(self):
        form = RecordForm(data=self.valid_data)
        self.assertTrue(form.is_valid(), form.errors)

    # Test form is invalid without required fields
    def test_form_invalid_without_required_fields(self):
        invalid_data = self.valid_data.copy()
        invalid_data.pop('title')
        form = RecordForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    # Test form creates a new record when saved
    def test_form_save_creates_record(self):
        form = RecordForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        record = form.save()
        self.assertIsInstance(record, Record)
        self.assertEqual(record.title, self.valid_data['title'])
        self.assertEqual(record.artist, self.artist)


class ArtistFormTest(TestCase):
    """
    Test Case for ArtistForm.
    """
    # Test form is valid with valid data
    @patch('cloudinary.uploader.upload')
    def test_form_valid_with_valid_data(self, mock_upload):
        # Mock Cloudinary upload to avoid external dependency
        mock_upload.return_value = {
            "public_id": "fake_id",
            "version": "1234567890",
            "signature": "fake_signature",
            "width": 100,
            "height": 100,
            "format": "jpg",
            "resource_type": "image",
            "created_at": "2025-09-09T00:00:00Z",
            "bytes": 1024,
            "type": "upload",
            "url": "http://res.cloudinary.com/demo/image/upload/fake_id.jpg",
            "secure_url": "https://res.cloudinary.com/demo/image/upload/fake_id.jpg"
        }

        data = {
            'name': 'Test Artist',
            'slug': 'test-artist',
            'debut_year': 2020,
            'bio': 'Test bio',
        }
        files = {
            'image': get_test_image_file()
        }
        form = ArtistForm(data=data, files=files)
        self.assertTrue(form.is_valid(), form.errors)
        artist = form.save()
        self.assertEqual(artist.name, 'Test Artist')

    # Test form is invalid without name
    def test_form_invalid_missing_name(self):
        files = {'image': get_test_image_file()}
        data = {
            'slug': 'test-artist',
            'debut_year': 2020,
            'bio': 'Test bio',
        }
        form = ArtistForm(data=data, files=files)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)


