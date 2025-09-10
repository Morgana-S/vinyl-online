from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
from .models import Order
from profiles.models import UserProfile, DeliveryAddress
from records.models import Record, Artist, Genre
import json


class CheckoutViewTest(TestCase):
    """
    TestCase for the checkout_view view.
    """

    def setUp(self):
        self.client = Client()
        # Create a test user with profile
        self.user = User.objects.create_user(
            username='testuser',
            email='user@example.com',
            password='password'
        )
        UserProfile.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            contact_phone_number='+441234567890',
            contact_email='user@example.com'
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
        self.url = reverse('checkout')
        # Pre-populate session basket
        session = self.client.session
        session['basket'] = {str(self.record.id): 2}
        session.save()

    # Tests that the checkout view can be reached as an authenticated user
    @patch('checkout.views.stripe.PaymentIntent.create')
    @patch('checkout.views.stripe.PaymentIntent.retrieve')
    def test_get_checkout_view_authenticated_user(
            self, mock_retrieve, mock_create):
        # Mock stripe PaymentIntent
        mock_intent = MagicMock()
        mock_intent.id = 'pi_123'
        mock_intent.client_secret = 'secret_123'
        mock_intent.status = 'requires_payment_method'
        mock_retrieve.return_value = mock_intent
        mock_create.return_value = mock_intent

        # Log in user
        self.client.login(username='testuser', password='password')

        response = self.client.get(reverse('checkout'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')
        self.assertIn('form', response.context)
        self.assertIn('client_secret', response.context)
        self.assertEqual(response.context['subtotal_cost'], Decimal('20.00'))
        self.assertEqual(response.context['delivery_cost'], Decimal('2.00'))
        self.assertEqual(response.context['grand_total'], Decimal('22.00'))

    # Tests that the order and orderitems are created - authorised user
    @patch('checkout.views.stripe.PaymentIntent.create')
    @patch('checkout.views.stripe.PaymentIntent.retrieve')
    @patch('checkout.views.send_mail')
    def test_post_checkout_creates_order_and_items(
            self, mock_send_mail, mock_retrieve, mock_create):
        # Mock Stripe PaymentIntent
        mock_intent = MagicMock()
        mock_intent.id = 'pi_123'
        mock_intent.client_secret = 'secret_123'
        mock_intent.status = 'requires_payment_method'
        mock_retrieve.return_value = mock_intent
        mock_create.return_value = mock_intent

        self.client.login(username='testuser', password='password')

        data = {
            'full_name': 'Test User',
            'phone_number': '+441234567890',
            'email': 'user@example.com',
            'address_line1': '123 Street',
            'address_line2': '',
            'city': 'London',
            'postcode': 'E1 6AN',
        }

        response = self.client.post(
            reverse('checkout'),
            data=json.dumps({'stripe_pid': 'pi_123', **data}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        resp_json = response.json()
        self.assertTrue(resp_json['success'])

        # Check Order created
        order = Order.objects.get(uuid=resp_json['order_uuid'])
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.subtotal_cost, Decimal('20.00'))
        self.assertEqual(order.delivery_cost, Decimal('2.00'))
        self.assertEqual(order.grand_total_cost,
                         order.subtotal_cost + order.delivery_cost)

        # Check OrderItem created
        items = order.items.all()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].record, self.record)
        self.assertEqual(items[0].quantity, 2)
        self.assertEqual(items[0].item_total, self.record.price * 2)

        # Basket should be cleared
        session = self.client.session
        self.assertEqual(session.get('basket'), {})

        # Email should be sent
        mock_send_mail.assert_called()

    # Tests that order and order item is created - guest user
    @patch('checkout.views.stripe.PaymentIntent.create')
    @patch('checkout.views.stripe.PaymentIntent.retrieve')
    @patch('checkout.views.send_mail')
    def test_guest_post_checkout_creates_order_and_items(
            self, mock_send_mail, mock_retrieve, mock_create):
        # Mock Stripe PaymentIntent
        mock_intent = MagicMock()
        mock_intent.id = 'pi_guest'
        mock_intent.client_secret = 'secret_guest'
        mock_intent.status = 'requires_payment_method'
        mock_retrieve.return_value = mock_intent
        mock_create.return_value = mock_intent

        data = {
            'full_name': 'Guest User',
            'phone_number': '+441234567890',
            'email': 'guest@example.com',
            'address_line1': '456 Guest St',
            'address_line2': '',
            'city': 'Manchester',
            'postcode': 'M1 2AB',
        }

        response = self.client.post(
            reverse('checkout'),
            data=json.dumps({'stripe_pid': 'pi_guest', **data}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        resp_json = response.json()
        self.assertTrue(resp_json['success'])

        # Check Order created without user
        order = Order.objects.get(uuid=resp_json['order_uuid'])
        self.assertIsNone(order.user)
        self.assertEqual(order.full_name, 'Guest User')
        self.assertEqual(order.address_line1, '456 Guest St')
        self.assertEqual(order.address_line2, '')
        self.assertEqual(order.city, 'Manchester')
        self.assertEqual(order.postcode, 'M1 2AB')
        self.assertEqual(order.email, 'guest@example.com')
        self.assertEqual(order.subtotal_cost, Decimal('20.00'))
        self.assertEqual(order.grand_total_cost,
                         order.subtotal_cost + order.delivery_cost)

        # Check OrderItem created
        items = order.items.all()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].record, self.record)
        self.assertEqual(items[0].quantity, 2)
        self.assertEqual(items[0].item_total, self.record.price * 2)

        # Basket should be cleared
        session = self.client.session
        self.assertEqual(session.get('basket'), {})

        # Email should be sent
        mock_send_mail.assert_called()

    # Tests that the user is redirected if basket is empty
    def test_redirect_if_basket_empty(self):
        session = self.client.session
        session['basket'] = {}
        session.save()

        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('index'))

        messages = list(response.wsgi_request._messages)
        self.assertTrue(any(
            "empty" in str(message) for message in messages
        ))

    # Tests that a new address is created when asked to do so
    @patch('checkout.views.stripe.PaymentIntent.create')
    @patch('checkout.views.stripe.PaymentIntent.retrieve')
    def test_post_creates_new_delivery_address(
            self, mock_retrieve, mock_create):
        # Mock Stripe PaymentIntent
        mock_intent = MagicMock()
        mock_intent.id = 'pi_123'
        mock_intent.client_secret = 'secret_123'
        mock_intent.status = 'requires_payment_method'
        mock_retrieve.return_value = mock_intent
        mock_create.return_value = mock_intent

        # Log in user
        self.client.login(username='testuser', password='password')

        data = {
            'full_name': 'Test User',
            'phone_number': '+441234567890',
            'email': 'user@example.com',
            'address_line1': '123 Street',
            'address_line2': 'Flat 5',
            'city': 'London',
            'postcode': 'E1 6AN',
            'save_new_address': True,
        }

        response = self.client.post(
            reverse('checkout'),
            data=json.dumps({'stripe_pid': 'pi_123', **data}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        resp_json = response.json()
        self.assertTrue(resp_json['success'])

        # Ensure DeliveryAddress created
        delivery_address = DeliveryAddress.objects.filter(
            user=self.user).first()
        self.assertIsNotNone(delivery_address)
        self.assertEqual(delivery_address.address_line1, '123 Street')
        self.assertEqual(delivery_address.address_line2, 'Flat 5')
        self.assertEqual(delivery_address.city, 'London')
        self.assertEqual(delivery_address.postcode, 'E1 6AN')

    # Tests that using an existing address does not duplicate it
    @patch('checkout.views.stripe.PaymentIntent.create')
    @patch('checkout.views.stripe.PaymentIntent.retrieve')
    def test_post_uses_existing_delivery_address(
            self, mock_retrieve, mock_create):
        # Mock Stripe PaymentIntent
        mock_intent = MagicMock()
        mock_intent.id = 'pi_456'
        mock_intent.client_secret = 'secret_456'
        mock_intent.status = 'requires_payment_method'
        mock_retrieve.return_value = mock_intent
        mock_create.return_value = mock_intent

        self.client.login(username='testuser', password='password')

        # Create an existing delivery address for this user
        existing_address = DeliveryAddress.objects.create(
            user=self.user,
            label='Home',
            address_line1='99 Old Street',
            address_line2='Apt 2',
            city='Bristol',
            postcode='BS1 4TB'
        )

        data = {
            'full_name': 'Test User',
            'phone_number': '+441234567890',
            'email': 'user@example.com',
            'saved_address': str(existing_address.pk),
            'address_line1': existing_address.address_line1,
            'postcode': existing_address.postcode,
            'save_new_address': False,
        }

        response = self.client.post(
            reverse('checkout'),
            data=json.dumps({'stripe_pid': 'pi_456', **data}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        resp_json = response.json()
        self.assertTrue(resp_json['success'])

        # Check that no *additional* DeliveryAddress was created
        self.assertEqual(
            DeliveryAddress.objects.filter(user=self.user).count(),
            1
        )

        # Ensure the order used the existing address values
        order = Order.objects.get(uuid=resp_json['order_uuid'])
        self.assertEqual(order.address_line1, existing_address.address_line1)
        self.assertEqual(order.city, existing_address.city)
        self.assertEqual(order.postcode, existing_address.postcode)


class OrderConfirmationViewTest(TestCase):
    """
    TestCase for order_confirmation_view.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
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
            stripe_pid='pi_test'
        )

        self.client = Client()
        self.url = reverse('order_confirmation', kwargs={
                           'order_uuid': self.order.uuid})

    # Test view renders, correct template is used
    def test_order_confirmation_view_renders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/order_confirmation.html')
        self.assertEqual(response.context['order'], self.order)
        self.assertFalse(response.context['from_checkout'])

    # Test view renders if directed from checkout
    def test_order_confirmation_view_with_from_checkout_true(self):
        response = self.client.get(self.url + '?from_checkout=True')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['from_checkout'])

    # Test status code 404 for invalid uuid
    def test_order_confirmation_view_invalid_uuid(self):
        invalid_url = reverse(
            'order_confirmation', kwargs={
                'order_uuid': '00000000-0000-0000-0000-000000000000'})
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 404)


class FullOrderHistoryViewTest(TestCase):
    """
    TestCase for full_order_history_view.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='testuser2@example.com',
            password='password123'
        )

        self.order1 = Order.objects.create(
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
            stripe_pid='pi_test2'
        )
        self.order2 = Order.objects.create(
            user=self.user,
            full_name='Test User',
            address_line1='123 Test St',
            address_line2='',
            city='Testville',
            postcode='T1 2ST',
            phone_number='+441234567890',
            email='testuser@example.com',
            subtotal_cost=Decimal('55.00'),
            delivery_cost=Decimal('5.50'),
            grand_total_cost=Decimal('60.50'),
            stripe_pid='pi_test'
        )

        # Create an order for another user to ensure it does not appear
        self.other_order = Order.objects.create(
            user=self.user2,
            full_name='Other User',
            address_line1='456 Other St',
            address_line2='',
            city='Otherville',
            postcode='O1 2OT',
            phone_number='+441112223334',
            email='otheruser@example.com',
            subtotal_cost=Decimal('20.00'),
            delivery_cost=Decimal('5.00'),
            grand_total_cost=Decimal('25.00'),
            stripe_pid='pi_test3'
        )

        self.url = reverse('order_history')

    # Tests redirect if not logged in
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    # Tests the view renders correctly for logged in user
    def test_view_renders_correct_template_for_logged_in_user(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/order_history.html')

    # Tests view returns only the user's orders
    def test_view_returns_only_user_orders(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.url)
        orders = response.context['orders']
        self.assertEqual(len(orders), 2)
        self.assertIn(self.order1, orders)
        self.assertIn(self.order2, orders)
        self.assertNotIn(self.other_order, orders)

    # Tests orders are shown in descending order
    def test_orders_are_ordered_by_created_at_descending(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.url)
        orders = list(response.context['orders'])
        self.assertEqual(orders, sorted(
            orders, key=lambda o: o.created_at, reverse=True))
