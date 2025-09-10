from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from checkout.models import Order, OrderItem
from .models import SupportTicket
from records.models import Review, Artist, Record, Genre
from .forms import SupportTicketForm, NewsletterSubscriptionForm, ReviewForm


class CreateSupportTicketViewTest(TestCase):
    """
    TestCase for create_support_ticket_view.
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.url = reverse('create_support_ticket')

    # Test that a logged in user renders the form
    def test_get_request_renders_form_authenticated(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'community/create_support_ticket.html')
        self.assertIsInstance(response.context['form'], SupportTicketForm)

    # Tests that a guest user renders the form
    def test_get_request_renders_form_guest(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'community/create_support_ticket.html')
        self.assertIsInstance(response.context['form'], SupportTicketForm)

    # Tests authenticated user can create support ticket
    @patch('community.views.send_mail')
    def test_post_authenticated_creates_ticket_and_sends_email(
            self, mock_send_mail):
        self.client.login(username='testuser', password='password123')
        data = {
            'name': 'Test User',
            'email': 'testuser@example.com',
            'category': 'feedback',
            'description': 'This is a test support ticket.'
        }
        response = self.client.post(self.url, data)

        # Check redirect
        self.assertRedirects(response, reverse('profile'))

        # Check ticket created
        ticket = SupportTicket.objects.get(user=self.user)
        self.assertEqual(ticket.name, data['name'])
        self.assertEqual(ticket.email, data['email'])
        self.assertEqual(ticket.category, data['category'])
        self.assertEqual(ticket.description, data['description'])

        # Check email sent
        mock_send_mail.assert_called_once()
        self.assertIn(
            ticket.email, mock_send_mail.call_args[0][3])

    # Tests guest user can create support ticket
    @patch('community.views.send_mail')
    def test_post_guest_creates_ticket_and_sends_email(
            self, mock_send_mail):
        data = {
            'name': 'Guest User',
            'email': 'guest@example.com',
            'category': 'other',
            'description': 'Guest ticket description.'
        }
        response = self.client.post(self.url, data)

        # Check redirect for guest
        self.assertRedirects(response, reverse('index'))

        # Check ticket created
        ticket = SupportTicket.objects.get(email='guest@example.com')
        self.assertEqual(ticket.name, data['name'])
        self.assertEqual(ticket.category, data['category'])
        self.assertEqual(ticket.description, data['description'])

        # Check email sent
        mock_send_mail.assert_called_once()
        self.assertIn(
            ticket.email, mock_send_mail.call_args[0][3])

    # Tests form has validation for missing fields
    def test_post_invalid_form_returns_errors(self):
        data = {'name': '', 'email': '', 'category': '', 'description': ''}
        response = self.client.post(reverse('create_support_ticket'), data)
        self.assertEqual(response.status_code, 400)
        json_data = response.json()
        self.assertIn('name', json_data['errors'])
        self.assertIn('This field is required.', json_data['errors']['name'])


class TicketDetailViewTest(TestCase):
    """
    TestCase for ticket_detail_view.
    """

    def setUp(self):
        self.ticket = SupportTicket.objects.create(
            name="Test User",
            email="testuser@example.com",
            category="Other",
            description="Test message"
        )

    # Tests ticket detail renders ticket correctly
    def test_ticket_detail_view_renders_ticket(self):
        url = reverse('ticket_detail', kwargs={'pk': self.ticket.uuid})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'community/ticket_detail.html')
        self.assertEqual(response.context['ticket'], self.ticket)
        self.assertContains(response, self.ticket.category)
        self.assertContains(response, self.ticket.description)


class SupportTicketHistoryView(TestCase):
    """
    TestCase for support_ticket_history_view.
    """

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="pass1234"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="pass1234"
        )

        # Create tickets for both users
        self.ticket1 = SupportTicket.objects.create(
            user=self.user1,
            name="User One",
            email="user1@example.com",
            category="Other",
            description="Issue from user1"
        )
        self.ticket2 = SupportTicket.objects.create(
            user=self.user2,
            name="User Two",
            email="user2@example.com",
            category="Billing",
            description="Issue from user2"
        )

        self.url = reverse("support_ticket_history")

    # Tests users only see their own tickets
    def test_logged_in_user_sees_own_tickets_only(self):
        self.client.login(username="user1", password="pass1234")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                "community/support_ticket_history.html")

        # Check that this user's ticket is shown
        self.assertContains(response, "open")
        self.assertContains(response, "Other")
        self.assertContains(response, str(self.ticket1.pk))

        # Check that other user's tickets are NOT shown
        self.assertNotContains(response, str(self.ticket2.pk))


class AboutPageViewTest(TestCase):
    """
    TestCase for the about_page_view.
    """
    # Tests template and page renders

    def test_about_page_renders_correct_template(self):
        url = reverse('about')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'community/about_us.html')


class NewsletterSubscribeViewTest(TestCase):
    """
    TestCase for the newsletter_subscribe_view.
    """

    def setUp(self):
        self.url = reverse('newsletter')
        self.user = User.objects.create_user(
            username='testuser', password='pass1234')

    # Test the form renders on a get request
    def test_get_request_renders_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'community/newsletter_subscribe.html')
        self.assertIsInstance(
            response.context['form'], NewsletterSubscriptionForm)

    # Test authenticated user can create a subscription
    @patch('community.views.send_mail')
    def test_post_authenticated_user_creates_subscription(
            self, mock_send_mail):
        self.client.login(username='testuser', password='pass1234')
        response = self.client.post(
            self.url, data={
                'name': 'test name',
                'email': 'test@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))
        self.assertTrue(mock_send_mail.called)

    # Test anonymous user can create a subscription
    @patch('community.views.send_mail')
    def test_post_anonymous_user_creates_subscription(self, mock_send_mail):
        response = self.client.post(
            self.url, data={
                'name': 'test name',
                'email': 'anon@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))
        self.assertTrue(mock_send_mail.called)


class AddReviewViewTest(TestCase):
    """
    TestCase for add_review_view.
    """

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='testuser',
            email='user@example.com',
            password='password'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='user2@example.com',
            password='password'
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
        self.order1 = Order.objects.create(
            user=self.user1,
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
            order=self.order1,
            record=self.record,
            quantity=1
        )
        self.review = Review.objects.create(
            author=self.user1,
            record=self.record,
            delivery_rating=5,
            quality_rating=5,
            record_rating=5,
            review_text="Great record!"
        )
        self.url = reverse("add_review", kwargs={
                           "record_slug": self.record.slug})

    # Tests the user is redirected if not logged in
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    # Tests eligibility to make review
    def test_user_can_access_review_form_if_eligible(self):
        # User2 has not purchased yet
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        # Redirected due to ineligible
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            "record_detail", kwargs={"record_slug": self.record.slug}))

        # User1 has purchased, but already reviewed → redirected
        self.client.login(username="testuser2", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            "record_detail", kwargs={"record_slug": self.record.slug}))

    # Tests posting a review after ordering
    def test_post_review_success(self):
        self.order2 = Order.objects.create(
            user=self.user2,
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
            order=self.order2,
            record=self.record,
            quantity=1
        )
        self.client.login(username="testuser2", password="password")
        response = self.client.post(self.url, {
            "delivery_rating": 5,
            "quality_rating": 5,
            "record_rating": 5,
            "review_text": "Great record!test"
        })
        # Should redirect after successful POST
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(
            author=self.user2, record=self.record).exists())

    # Test that a user can't post if they haven't purchased
    def test_user_cannot_review_without_purchase(self):
        self.client.login(username="testuser2", password="password")
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse(
            "record_detail", kwargs={"record_slug": self.record.slug}))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(
            str(messages[0]),
            'You must purchase this record in order to provide a review.')

    # Tests that a user can't review twice
    def test_user_cannot_review_twice(self):

        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse(
            "record_detail", kwargs={"record_slug": self.record.slug}))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(
            str(messages[0]),
            'You have already provided a review for this record.')


class DeleteReviewViewTest(TestCase):
    """
    TestCase for delete_review_view.
    """

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='testuser',
            email='user@example.com',
            password='password'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='user2@example.com',
            password='password'
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
        self.order1 = Order.objects.create(
            user=self.user1,
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
            order=self.order1,
            record=self.record,
            quantity=1
        )
        self.review = Review.objects.create(
            author=self.user1,
            record=self.record,
            delivery_rating=5,
            quality_rating=5,
            record_rating=5,
            review_text="Great record!"
        )
        self.url = reverse("delete_review", kwargs={
                           "review_id": self.review.pk})

    # Tests author can delete their review
    def test_author_can_delete_review(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(self.url)

        # Review should be deleted
        self.assertFalse(Review.objects.filter(pk=self.review.pk).exists())
        # Redirect back to record detail
        self.assertRedirects(response, reverse(
            "record_detail", kwargs={"record_slug": self.record.slug}))

    # Tests user who isn't the author can't delete review
    def test_non_author_cannot_delete_review(self):
        self.client.login(username="testuser2", password="password")
        response = self.client.post(self.url)

        # Review should still exist
        self.assertTrue(Review.objects.filter(pk=self.review.pk).exists())
        # Redirect back to record detail
        self.assertRedirects(response, reverse(
            "record_detail", kwargs={"record_slug": self.record.slug}))
        # Check for error message
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any("not the author" in str(m) for m in messages))

    # Tests anonymous users are redirected to login
    def test_anonymous_user_redirected_to_login(self):
        response = self.client.post(self.url)
        login_url = reverse("account_login")
        self.assertRedirects(response, f"{login_url}?next={self.url}")


class PrivacyPolicyViewTest(TestCase):
    """
    TestCase for privacy_policy_view.
    """

    def setUp(self):
        self.url = reverse("privacy_policy")

    # Tests privacy policy renders correctly
    def test_privacy_policy_page_renders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "community/privacy_policy.html")
        self.assertContains(response, "Privacy Policy")


class ReturnPolicyViewTest(TestCase):
    """
    TestCase for return_policy_view.
    """

    def setUp(self):
        self.url = reverse("return_policy")

    # Tests privacy policy renders correctly
    def test_privacy_policy_page_renders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "community/return_policy.html")
        self.assertContains(response, "Return Policy")


class TermsOfServiceViewTest(TestCase):
    """
    TestCase for terms_of_service_view.
    """

    def setUp(self):
        self.url = reverse("terms_of_service")

    # Tests privacy policy renders correctly
    def test_privacy_policy_page_renders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "community/terms_of_service.html")
        self.assertContains(response, "Terms of Service")
