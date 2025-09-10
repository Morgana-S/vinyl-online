from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import UserProfile, DeliveryAddress

# Create your tests here.


class UserProfileModelTest(TestCase):
    """
    TestCase for the UserProfile model.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password123',
            email='user@example.com'
        )

    # Test a user profile is created
    def test_create_user_profile(self):
        profile = UserProfile.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            contact_phone_number='+441234567890'
        )
        self.assertEqual(profile.user.username, 'testuser')
        self.assertEqual(profile.first_name, 'John')
        self.assertEqual(profile.last_name, 'Doe')
        self.assertEqual(profile.contact_phone_number.as_e164, '+441234567890')

    # Tests that the contact email defaults to the user email
    def test_contact_email_defaults_to_user_email(self):
        profile = UserProfile.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            contact_phone_number='+441234567890'
        )
        self.assertEqual(profile.contact_email, 'user@example.com')

    # Tests __str__ returns username
    def test_str_method_returns_username(self):
        profile = UserProfile.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            contact_phone_number='+441234567890'
        )
        self.assertEqual(str(profile), 'testuser')

    # Tests that the full_name method works
    def test_full_name_method(self):
        profile = UserProfile.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            contact_phone_number='+441234567890'
        )
        self.assertEqual(profile.full_name(), 'John Doe')

    # Tests that the validation is working
    def test_min_length_validation(self):
        profile = UserProfile(
            user=self.user,
            first_name='',
            last_name='D',
            contact_phone_number='+441234567890'
        )
        with self.assertRaises(ValidationError):
            profile.full_clean()  # triggers model validators

        profile = UserProfile(
            user=self.user,
            first_name='J',
            last_name='',
            contact_phone_number='+441234567890'
        )
        with self.assertRaises(ValidationError):
            profile.full_clean()


class DeliveryAddressModelTest(TestCase):
    """
    TestCase for the DeliveryAddress model.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password123',
            email='user@example.com'
        )

    # Tests whether an address is created successfully
    def test_create_address(self):
        address = DeliveryAddress.objects.create(
            user=self.user,
            label='Home',
            address_line1='123 Main Street',
            address_line2='Flat 1',
            city='London',
            postcode='E1 6AN'
        )
        self.assertEqual(address.user.username, 'testuser')
        self.assertEqual(address.label, 'Home')
        self.assertEqual(address.address_line1, '123 Main Street')
        self.assertEqual(address.address_line2, 'Flat 1')
        self.assertEqual(address.city, 'London')
        self.assertEqual(address.postcode, 'E1 6AN')

    # Tests optional fields can be blank
    def test_optional_fields_can_be_blank(self):
        address = DeliveryAddress.objects.create(
            user=self.user,
            label='Work',
            address_line1='456 Office Road',
            postcode='SW1A 1AA'
        )
        self.assertEqual(address.address_line2, '')
        self.assertEqual(address.city, '')

    # Tests __str__ returns label
    def test_str_method_returns_label(self):
        address = DeliveryAddress.objects.create(
            user=self.user,
            label='Home',
            address_line1='123 Main Street',
            postcode='E1 6AN'
        )
        self.assertEqual(str(address), 'Home')

    # Tests validation
    def test_required_fields_validation(self):
        address = DeliveryAddress(user=self.user, label='Home')
        with self.assertRaises(ValidationError):
            address.full_clean()
