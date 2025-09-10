from django.contrib.auth.models import User
from django.test import TestCase
from .forms import SupportTicketForm, NewsletterSubscriptionForm, ReviewForm
from .models import SupportTicket, NewsletterSubscriber
from records.models import Record, Artist, Genre
from profiles.models import UserProfile


class SupportTicketFormTest(TestCase):
    """
    TestCase for the SupportTicketForm.
    """

    def setUp(self):
        # Create a test user
        self.user_with_profile = User.objects.create_user(
            username='profileuser',
            password='password123',
            email='userprofile@example.com'
        )

        self.profile = UserProfile.objects.create(
            user=self.user_with_profile,
            first_name='Test',
            last_name='User',
            contact_phone_number='+447700900123',
            contact_email='profilecontact@example.com'
        )

        # User without a profile
        self.user_without_profile = User.objects.create_user(
            username='noprofileuser',
            password='password123',
            email='noprof@example.com'
        )

        self.valid_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'category': 'payment',
            'description': 'I have an issue with billing.'
        }

    # Tests form with valid data
    def test_form_valid_with_valid_data(self):
        form = SupportTicketForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    # Tests form isn't valid without required fields
    def test_form_invalid_without_required_fields(self):
        form = SupportTicketForm(data={})
        self.assertFalse(form.is_valid())
        for field in ['name', 'email', 'category', 'description']:
            self.assertIn(field, form.errors)

    # Test form prepopulates with values from user profile
    def test_initial_values_prefilled_from_user_profile(self):
        form = SupportTicketForm(user=self.user_with_profile)
        self.assertEqual(form.fields['name'].initial, self.profile.full_name())
        self.assertEqual(form.fields['email'].initial,
                         self.profile.contact_email)

    # Tests form falls back to user email if they have no profile
    def test_initial_values_fallback_to_user_email_if_no_profile(self):
        form = SupportTicketForm(user=self.user_without_profile)
        self.assertIsNone(form.fields['name'].initial)
        self.assertEqual(form.fields['email'].initial,
                         self.user_without_profile.email)

    # Tests form creates support ticket on save
    def test_form_save_creates_support_ticket(self):
        form = SupportTicketForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        ticket = form.save()
        self.assertIsInstance(ticket, SupportTicket)
        self.assertEqual(ticket.name, self.valid_data['name'])
        self.assertEqual(ticket.email, self.valid_data['email'])
        self.assertEqual(ticket.category, self.valid_data['category'])
        self.assertEqual(ticket.description, self.valid_data['description'])
        self.assertEqual(ticket.status, 'open')

    # Tests form saves with associated user
    def test_form_save_with_user_association(self):
        data = self.valid_data.copy()
        form = SupportTicketForm(data=data, user=self.user_with_profile)
        self.assertTrue(form.is_valid())
        ticket = form.save(commit=False)
        ticket.user = self.user_with_profile
        ticket.save()
        self.assertEqual(ticket.user, self.user_with_profile)


class NewsletterSubscriptionFormTest(TestCase):
    """
    TestCase for the NewsletterSubscriptionForm.
    """

    def setUp(self):
        # Create a user for tests
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        # Sample valid data
        self.valid_data = {
            'name': 'Test User',
            'email': 'subscriber@example.com'
        }

    # Tests form is valid with data
    def test_form_valid_with_valid_data(self):
        form = NewsletterSubscriptionForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    # Tests that the form is invalid when the name is missing
    def test_form_invalid_missing_name(self):
        data = self.valid_data.copy()
        data.pop('name')
        form = NewsletterSubscriptionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    # Tests that form is invalid when email is missing
    def test_form_invalid_missing_email(self):
        data = self.valid_data.copy()
        data.pop('email')
        form = NewsletterSubscriptionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    # Tests that an existing subscriber can't create a duplicate record
    def test_form_invalid_duplicate_email(self):
        NewsletterSubscriber.objects.create(
            name='Someone', email=self.valid_data['email'])
        form = NewsletterSubscriptionForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(
            form.errors['email'][0],
            "This email address is already subscribed to the newsletter."
        )

    # Tests forms prepopulate when user has a UserProfile
    def test_form_prefills_authenticated_user_profile(self):
        # Add a profile to user
        UserProfile.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            contact_email='profile@example.com',
            contact_phone_number='+44123456790'
        )

        form = NewsletterSubscriptionForm(user=self.user)
        self.assertEqual(form.fields['name'].initial, "Test User")
        self.assertEqual(form.fields['email'].initial, "profile@example.com")

    # Tests form populates email if user doesn't have a userprofile
    def test_form_prefills_authenticated_user_without_profile(self):
        form = NewsletterSubscriptionForm(user=self.user)
        self.assertEqual(form.fields['email'].initial, self.user.email)


class ReviewFormTest(TestCase):
    """
    TestCase for the ReviewForm.
    """

    def setUp(self):
        # Create a user and a record to attach reviews to
        self.user = User.objects.create_user(
            username='reviewer',
            email='reviewer@example.com',
            password='password'
        )
        self.artist = Artist.objects.create(
            name='Test Artist',
            slug='test-artist'
        )
        self.genre1 = Genre.objects.create(
            name='Pop',
            color='#FFFFFF',
            description='test'
        )
        self.record = Record.objects.create(
            title='Test Album',
            artist=self.artist,
            price=10.99,
            slug='test-album',
            quantity=5,
            hidden=False,
        )
        self.record.genre.set([self.genre1])

        # Valid review form data
        self.valid_data = {
            'delivery_rating': 5,
            'quality_rating': 4,
            'record_rating': 5,
            'store_feedback': 'Great service!',
            'review_text': 'Loved the album!',
        }

    # Test form data is valid
    def test_form_valid_with_all_fields(self):
        form = ReviewForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    # Tests form is valid when optional fields don't exist
    def test_form_valid_without_optional_fields(self):
        data = self.valid_data.copy()
        data.pop('store_feedback')
        data.pop('review_text')
        form = ReviewForm(data=data)
        self.assertTrue(form.is_valid())

    # Tests form is invalid when the delivery rating is missing
    def test_form_invalid_missing_delivery_rating(self):
        data = self.valid_data.copy()
        data.pop('delivery_rating')
        form = ReviewForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('delivery_rating', form.errors)

    # Tests form is invalid when missing quality rating
    def test_form_invalid_missing_quality_rating(self):
        data = self.valid_data.copy()
        data.pop('quality_rating')
        form = ReviewForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('quality_rating', form.errors)

    # Tests form is invalid when missing record rating
    def test_form_invalid_missing_record_rating(self):
        data = self.valid_data.copy()
        data.pop('record_rating')
        form = ReviewForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('record_rating', form.errors)
