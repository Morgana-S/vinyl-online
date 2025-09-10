from django.contrib.auth.models import User
from django.test import TestCase
from .forms import UserProfileForm, DeliveryAddressForm
from .models import DeliveryAddress


class UserProfileFormTest(TestCase):
    """
    TestCase for the UserProfileForm.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='password')
        self.valid_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'contact_email': 'john.doe@example.com',
            'contact_phone_number': '+441234567890',
        }

    # Tests form is valid with all required fields
    def test_form_valid_with_all_required_fields(self):
        form = UserProfileForm(data=self.valid_data)
        self.assertTrue(form.is_valid(), form.errors)

    # Tests form is invalid if first name is missing
    def test_form_invalid_missing_first_name(self):
        data = self.valid_data.copy()
        data['first_name'] = ''
        form = UserProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)

    # Tests form is invalid if last name is missing
    def test_form_invalid_missing_last_name(self):
        data = self.valid_data.copy()
        data['last_name'] = ''
        form = UserProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)

    # Tests form is invalid if missing phone number
    def test_form_invalid_missing_contact_phone_number(self):
        data = self.valid_data.copy()
        data['contact_phone_number'] = ''
        form = UserProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('contact_phone_number', form.errors)

    # Tests contact email is allowed to stay blank
    def test_optional_contact_email_can_be_blank(self):
        data = self.valid_data.copy()
        data['contact_email'] = ''
        form = UserProfileForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    # Tests that the saved form creates a user profile
    def test_form_save_creates_user_profile(self):
        form = UserProfileForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        profile = form.save(commit=False)
        profile.user = self.user
        profile.save()
        self.assertEqual(profile.first_name, self.valid_data['first_name'])
        self.assertEqual(profile.last_name,
                         self.valid_data['last_name'])
        self.assertEqual(profile.contact_email,
                         self.valid_data['contact_email'])
        self.assertEqual(
            str(profile.contact_phone_number),
            self.valid_data['contact_phone_number'])


class DeliveryAddressFormTest(TestCase):
    """
    TestCase for the DeliveryAddressForm.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='password')

        self.valid_data = {
            'label': 'Home',
            'address_line1': '123 Main St',
            'address_line2': 'Flat 4B',
            'city': 'London',
            'postcode': 'E1 6AN',
        }

        self.partial_data = {
            'label': 'Office',
            'address_line1': '456 High St',
            'postcode': 'SW1A 1AA',
        }

        self.invalid_data = {
            'label': '',  # missing
            'address_line1': '',  # missing
            'postcode': '',  # missing
        }

    # Tests if form is valid with all fields
    def test_form_valid_with_all_fields(self):
        form = DeliveryAddressForm(data=self.valid_data)
        self.assertTrue(form.is_valid(), form.errors)

        address = form.save(commit=False)
        address.user = self.user
        address.save()

        self.assertEqual(DeliveryAddress.objects.count(), 1)
        self.assertEqual(address.label, self.valid_data['label'])
        self.assertEqual(address.city, self.valid_data['city'])

    # Tests if form is valid with address_line2 and city missing
    def test_form_valid_with_partial_fields(self):
        form = DeliveryAddressForm(data=self.partial_data)
        self.assertTrue(form.is_valid(), form.errors)

        address = form.save(commit=False)
        address.user = self.user
        address.save()

        self.assertEqual(DeliveryAddress.objects.count(), 1)
        self.assertEqual(address.address_line2, '')  # Optional field empty
        self.assertEqual(address.city, '')  # Optional field empty

    # Tests form is invalid if required fields are missing
    def test_form_invalid_missing_required_fields(self):
        form = DeliveryAddressForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('label', form.errors)
        self.assertIn('address_line1', form.errors)
        self.assertIn('postcode', form.errors)
