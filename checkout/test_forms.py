from django.contrib.auth.models import User
from django.test import TestCase
from .forms import CheckoutForm
from profiles.models import DeliveryAddress, UserProfile


class CheckoutFormTest(TestCase):
    """
    TestCase for the CheckoutForm.
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password123",
            email="user@example.com"
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            contact_phone_number="+441234567890",
            contact_email="profile@example.com",
            first_name="John",
            last_name="Doe"
        )
        self.address = DeliveryAddress.objects.create(
            user=self.user,
            address_line1="123 Street",
            address_line2="",
            city="Testville",
            postcode="AB12CD"
        )

        self.valid_data = {
            "full_name": "Jane Doe",
            "phone_number": "+441987654321",
            "email": "jane@example.com",
            "address_line1": "456 Avenue",
            "address_line2": "Apt 7",
            "city": "Citytown",
            "postcode": "ZX98YX",
            "subtotal_cost": "10.00",
            "delivery_cost": "2.00",
            "grand_total_cost": "12.00",
            "stripe_pid": "stripepid"
        }

    # Tests form is valid with auth user with profile
    def test_form_valid_with_authenticated_user_and_profile(self):
        form = CheckoutForm(data=self.valid_data, user=self.user)
        self.assertTrue(form.is_valid())
        # Saved address queryset should include the address
        self.assertIn(self.address, form.fields['saved_address'].queryset)
        # Profile data should be set as initial values
        self.assertEqual(
            form.fields['phone_number'].initial,
            self.profile.contact_phone_number
        )
        self.assertEqual(form.fields['email'].initial,
                         self.profile.contact_email)
        self.assertEqual(
            form.fields['full_name'].initial, self.profile.full_name())

    # Test form is valid with anonymous user
    def test_form_valid_with_anonymous_user(self):
        form = CheckoutForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        # Anonymous users should not see saved_address field
        self.assertNotIn("saved_address", form.fields)

    # Test form is invalid without required fields
    def test_form_invalid_without_required_fields(self):
        invalid_data = {
            "full_name": "",
            "phone_number": "",
            "email": "",
            "address_line1": "",
            "city": "",
            "postcode": "",
        }
        form = CheckoutForm(data=invalid_data, user=self.user)
        self.assertFalse(form.is_valid())
        # Required fields should raise errors
        self.assertIn("full_name", form.errors)
        self.assertIn("phone_number", form.errors)
        self.assertIn("email", form.errors)
        self.assertIn("address_line1", form.errors)
        self.assertIn("postcode", form.errors)
