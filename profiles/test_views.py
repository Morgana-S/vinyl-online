from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from checkout.models import Order, OrderItem
from community.models import SupportTicket
from records.models import Artist, Genre, Record
from .models import UserProfile, DeliveryAddress
from .forms import UserProfileForm


class UserProfileViewTest(TestCase):
    """
    TestCase for user_profile_view.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='user@example.com',
            password='password'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            contact_phone_number="+441234567890",
            contact_email="user@example.com"
        )
        self.address = DeliveryAddress.objects.create(
            user=self.user,
            address_line1="123 Test Street",
            postcode="TE5 7ST"
        )
        self.artist = Artist.objects.create(
            name='Test Artist',
            slug='test-artist'
        )
        self.genre = Genre.objects.create(
            name='Pop',
            color='#FFFFFF',
            description='Test'
        )
        self.record = Record.objects.create(
            title='Test Record',
            slug='test-record',
            artist=self.artist,
            price=Decimal('10.00'),
            quantity=5
        )
        self.order = Order.objects.create(
            user=self.user,
            full_name='Test User',
            address_line1='123 Test St',
            address_line2='',
            city='Testville',
            postcode='T1 2ST',
            phone_number='+441234567890',
            email='testuser@example.com',
            subtotal_cost=Decimal('50.00'),
            delivery_cost=Decimal('5.00'),
            grand_total_cost=Decimal('55.00'),
            stripe_pid='pi_test2',
            status='delivered'
        )
        OrderItem.objects.create(
            order=self.order,
            record=self.record,
            quantity=1
        )
        self.ticket = SupportTicket.objects.create(
            user=self.user,
            name="Test User",
            email="testuser@example.com",
            category="Other",
            description="Test ticket"
        )
        self.url = reverse("profile")

    # Tests redirect if not logged in
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    # Tests authenticated user can access profile
    def test_authenticated_user_can_access_profile(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/profile.html")

        # Verify context data
        self.assertEqual(response.context['profile'], self.profile)
        self.assertIn(self.address, response.context['addresses'])
        self.assertIn(self.ticket, response.context['support_tickets'])
        self.assertIn(self.order, response.context['order_history'])


class CreateEditProfileViewTest(TestCase):
    """
    TestCase for create_edit_profile_view.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='user@example.com',
            password='password'
        )
        self.url = reverse("create_edit_profile")

    # Tests anonymous users are directed to log in
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    # Test logged in user can access form
    def test_authenticated_user_can_access_form(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/create_edit_profile.html")
        self.assertIsInstance(response.context['form'], UserProfileForm)
        self.assertIsInstance(response.context['profile'], UserProfile)

    # Test creation/update of profile
    def test_post_creates_or_updates_profile(self):
        self.client.login(username="testuser", password="password")
        post_data = {
            "first_name": "Test",
            "last_name": "User",
            "contact_phone_number": "+441234567890",
            "contact_email": "testuser@example.com"
        }
        response = self.client.post(self.url, data=post_data)
        self.assertRedirects(response, reverse("profile"))

        # Verify profile was created/updated
        profile = UserProfile.objects.get(user=self.user)
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.first_name, "Test")
        self.assertEqual(profile.last_name, "User")
        self.assertEqual(str(profile.contact_phone_number), "+441234567890")
        self.assertEqual(profile.contact_email, "testuser@example.com")


class CreateDeliveryAddressViewTest(TestCase):
    """
    TestCase for create_delivery_address_view.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.url = reverse("add_delivery_address")

    # Test logged in user renders form
    def test_get_renders_form(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "profiles/create_delivery_address.html")
        self.assertIn("form", response.context)

    # Test creating an address
    def test_post_creates_address_and_redirects(self):
        self.client.login(username="testuser", password="testpass123")

        post_data = {
            "label": "Home",
            "address_line1": "123 Main Street",
            "address_line2": "Flat 1",
            "city": "London",
            "postcode": "SW1A 1AA",
        }

        response = self.client.post(self.url, post_data)

        # Should redirect to the profile page
        self.assertRedirects(response, reverse("profile"))

        # Verify the address was created
        address = DeliveryAddress.objects.get(user=self.user)
        self.assertEqual(address.label, "Home")
        self.assertEqual(address.address_line1, "123 Main Street")
        self.assertEqual(address.address_line2, "Flat 1")
        self.assertEqual(address.city, "London")
        self.assertEqual(address.postcode, "SW1A 1AA")

    # Tests posting is invalid if form is not valid
    def test_post_invalid_data_rerenders_form_with_errors(self):
        self.client.login(username="testuser", password="testpass123")

        # Missing required address_line1
        post_data = {
            "label": "Home",
            "address_line1": "",
            "address_line2": "",
            "city": "London",
            "postcode": "SW1A 1AA",
        }

        response = self.client.post(self.url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "profiles/create_delivery_address.html")
        # Access the form from response context
        form = response.context["form"]
        self.assertTrue(form.errors)
        self.assertIn("address_line1", form.errors)
        self.assertEqual(form.errors["address_line1"],
                         ["This field is required."])


class EditDeliveryAddressView(TestCase):
    """
    TestCase for edit_delivery_address_view.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.address = DeliveryAddress.objects.create(
            user=self.user,
            label="Home",
            address_line1="123 Main St",
            address_line2="Apt 4",
            city="London",
            postcode="SW1A 1AA"
        )
        self.url = reverse("edit_delivery_address", args=[self.address.pk])

    # Test form renders with existing data
    def test_get_renders_form_with_existing_data(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "profiles/edit_delivery_address.html")
        self.assertIn("form", response.context)
        form = response.context["form"]
        self.assertEqual(form.instance, self.address)

    # Test updated with valid address redirects properly
    def test_post_valid_data_updates_address_and_redirects(self):
        self.client.login(username="testuser", password="testpass123")
        post_data = {
            "label": "Work",
            "address_line1": "456 Park Ave",
            "address_line2": "",
            "city": "London",
            "postcode": "E1 6AN"
        }
        response = self.client.post(self.url, post_data)
        self.address.refresh_from_db()
        self.assertEqual(self.address.label, "Work")
        self.assertEqual(self.address.address_line1, "456 Park Ave")
        self.assertRedirects(response, reverse("profile"))

    # Test invalid data renders form with errors
    def test_post_invalid_data_rerenders_form_with_errors(self):
        self.client.login(username="testuser", password="testpass123")
        post_data = {
            "label": "Work",
            "address_line1": "",
            "address_line2": "",
            "city": "London",
            "postcode": "E1 6AN"
        }
        response = self.client.post(self.url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "profiles/edit_delivery_address.html")
        form = response.context["form"]
        self.assertTrue(form.errors)
        self.assertIn("address_line1", form.errors)
        self.assertEqual(form.errors["address_line1"], [
                         "This field is required."])


class DeleteDeliveryAddressView(TestCase):
    """
    TestCase for delete_delivery_address_view.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", password="otherpass123"
        )
        self.address = DeliveryAddress.objects.create(
            user=self.user,
            label="Home",
            address_line1="123 Main St",
            address_line2="Apt 4",
            city="London",
            postcode="SW1A 1AA"
        )
        self.other_address = DeliveryAddress.objects.create(
            user=self.other_user,
            label="Office",
            address_line1="456 Park Ave",
            address_line2="Suite 1",
            city="London",
            postcode="E1 6AN"
        )
        self.url = reverse("delete_delivery_address", args=[self.address.pk])
        self.other_url = reverse("delete_delivery_address", args=[
                                 self.other_address.pk])

    # Tests posting deletes the address
    def test_post_deletes_address_and_redirects(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(self.url)
        self.assertFalse(DeliveryAddress.objects.filter(
            pk=self.address.pk).exists())
        self.assertRedirects(response, reverse("profile"))

    # Tests GET request redirects without deleting
    def test_get_request_redirects_without_deletion(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertTrue(DeliveryAddress.objects.filter(
            pk=self.address.pk).exists())
        self.assertRedirects(response, reverse("profile"))

    # Tests users can't delete other users addresses
    def test_user_cannot_delete_others_address(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(self.other_url)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(DeliveryAddress.objects.filter(
            pk=self.other_address.pk).exists())
