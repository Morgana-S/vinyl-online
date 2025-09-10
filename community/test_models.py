from django.contrib.auth.models import User
from django.test import TestCase
from .models import SupportTicket, NewsletterSubscriber
# Create your tests here.


class SupportTicketModelTest(TestCase):
    """
    TestCase for the SupportTicket model.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password123',
            email='user@example.com'
        )

    # Tests that a support ticket is created with user
    def test_create_support_ticket_with_user(self):
        ticket = SupportTicket.objects.create(
            user=self.user,
            name='John Doe',
            email='johndoe@example.com',
            category='delivery',
            description='My order has not arrived yet.'
        )

        self.assertEqual(ticket.user, self.user)
        self.assertEqual(ticket.name, 'John Doe')
        self.assertEqual(ticket.email, 'johndoe@example.com')
        self.assertEqual(ticket.category, 'delivery')
        self.assertEqual(ticket.description, 'My order has not arrived yet.')
        self.assertEqual(ticket.status, 'open')
        self.assertIsNotNone(ticket.created_at)
        self.assertIsNotNone(ticket.uuid)

    # Tests that a support ticket is created with no user
    def test_create_support_ticket_without_user(self):
        ticket = SupportTicket.objects.create(
            name='Jane Smith',
            email='janesmith@example.com',
            category='feedback',
            description='I love your store!'
        )

        self.assertIsNone(ticket.user)
        self.assertEqual(ticket.name, 'Jane Smith')
        self.assertEqual(ticket.category, 'feedback')
        self.assertEqual(ticket.status, 'open')

    # Tests that the default status for a ticket is 'open'
    def test_support_ticket_default_status(self):
        ticket = SupportTicket.objects.create(
            name='Anonymous',
            email='anon@example.com',
            category='other',
            description='Testing default status.'
        )
        self.assertEqual(ticket.status, 'open')

    # Tests that __str__ returns uuid + status
    def test_string_representation(self):
        ticket = SupportTicket.objects.create(
            name='Alice',
            email='alice@example.com',
            category='payment',
            description='Payment issue.'
        )
        # Default string representation could be name + email
        self.assertEqual(str(ticket), f'{ticket.uuid} - {ticket.status}')


class NewsletterSubscriberModelTest(TestCase):
    """
    TestCase for the NewsletterSubscriber model.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password123",
            email="user@example.com"
        )

    # Tests subscription created with authenticated user
    def test_create_subscriber_with_user(self):
        subscriber = NewsletterSubscriber.objects.create(
            user=self.user,
            name="John Doe",
            email="john@example.com"
        )

        self.assertEqual(subscriber.user, self.user)
        self.assertEqual(subscriber.name, "John Doe")
        self.assertEqual(subscriber.email, "john@example.com")

    # Tests subscription created with anonymous user
    def test_create_subscriber_without_user(self):
        subscriber = NewsletterSubscriber.objects.create(
            name="Anonymous",
            email="anon@example.com"
        )

        self.assertIsNone(subscriber.user)
        self.assertEqual(subscriber.name, "Anonymous")
        self.assertEqual(subscriber.email, "anon@example.com")

    # Tests that a user can't subscribe to the newsletter mutliple times
    def test_user_uniqueness_constraint(self):
        # First subscription with user succeeds
        NewsletterSubscriber.objects.create(
            user=self.user, email="first@example.com")

        # Attempting a second subscription for the same user should fail
        with self.assertRaises(Exception):
            NewsletterSubscriber.objects.create(
                user=self.user, email="second@example.com")
