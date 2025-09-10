from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import Order, OrderItem
from records.models import Record, Artist, Genre
# Create your tests here.


class OrderModelTest(TestCase):
    """
    TestCase for the Order model.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="user@example.com",
            password="password123"
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
        self.record_above_threshold = Record.objects.create(
            title='Test Record',
            slug='test-record',
            artist=self.artist,
            price=Decimal('105.00'),
            quantity=5
            )
        self.record_above_threshold.genre.set([self.genre])
        self.record_below_threshold = Record.objects.create(
            title='Test Record 2',
            slug='test-record-2',
            artist=self.artist,
            price=Decimal('10.00'),
            quantity=5
        )
        self.record_below_threshold.genre.set([self.genre])
        self.order = Order.objects.create(
            user=self.user,
            full_name="John Doe",
            address_line1="123 Main Street",
            address_line2="",
            city="London",
            postcode="SW1A 1AA",
            phone_number="+441234567890",
            email="john@example.com",
            subtotal_cost=Decimal("20.00"),
            delivery_cost=Decimal("5.00"),
            grand_total_cost=Decimal("25.00"),
            stripe_pid="test_stripe_pid_123",
        )

    # Tests order returns correct __str__
    def test_str_representation(self):
        self.assertIn(str(self.order.uuid), str(self.order))
        self.assertIn("25.00", str(self.order))

    # Tests order stores fields correctly
    def test_order_fields(self):
        self.assertEqual(self.order.full_name, "John Doe")
        self.assertEqual(self.order.city, "London")
        self.assertEqual(self.order.postcode, "SW1A 1AA")
        self.assertEqual(self.order.phone_number, "+441234567890")
        self.assertEqual(self.order.email, "john@example.com")
        self.assertEqual(self.order.subtotal_cost, Decimal("20.00"))
        self.assertEqual(self.order.delivery_cost, Decimal("5.00"))
        self.assertEqual(self.order.grand_total_cost, Decimal("25.00"))
        self.assertEqual(self.order.stripe_pid, "test_stripe_pid_123")

    # Tests if the order calculates delivery if below threshold
    def test_update_total_below_free_delivery_threshold(self):
        OrderItem.objects.create(
            order=self.order,
            record=self.record_below_threshold,
            quantity=2)
        self.order.update_total()

        self.assertEqual(self.order.subtotal_cost, Decimal("20.00"))
        if Decimal("20.00") < settings.FREE_DELIVERY_THRESHOLD:
            expected_delivery = Decimal(
                "20.00") * Decimal(settings.STANDARD_DELIVERY_MODIFIER)
            self.assertEqual(self.order.delivery_cost, expected_delivery)
            self.assertEqual(
                self.order.grand_total_cost,
                Decimal("20.00") + expected_delivery
            )

    # Tests if the order calculates delivery as three if above threshold
    def test_update_total_above_free_delivery_threshold(self):
        OrderItem.objects.create(
            order=self.order,
            record=self.record_above_threshold,
            quantity=1,
            item_total=Decimal('105.00'))

        self.order.update_total()

        self.assertGreaterEqual(self.order.subtotal_cost,
                                settings.FREE_DELIVERY_THRESHOLD)
        self.assertEqual(self.order.delivery_cost, Decimal("0"))
        self.assertEqual(self.order.grand_total_cost, self.order.subtotal_cost)


class OrderItemTest(TestCase):
    """
    TestCase for the OrderItem model.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="user@example.com",
            password="password123"
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
            full_name="John Doe",
            address_line1="123 Main Street",
            city="London",
            postcode="SW1A 1AA",
            phone_number="+441234567890",
            email="john@example.com",
            subtotal_cost=Decimal("0.00"),
            delivery_cost=Decimal("0.00"),
            grand_total_cost=Decimal("0.00"),
            stripe_pid="test_stripe_pid_123",
        )

    # Tests __str__ is correct
    def test_str_representation(self):
        item = OrderItem.objects.create(
            order=self.order, record=self.record, quantity=2)
        expected_str = f"{self.record.title} x 2 - Order: {self.order.uuid}"
        self.assertEqual(str(item), expected_str)

    # Tests item total is calculated when saved
    def test_item_total_is_calculated_on_save(self):
        item = OrderItem.objects.create(
            order=self.order, record=self.record, quantity=3)
        self.assertEqual(item.item_total, Decimal("30.00"))

    # Tests item total updates when quantity changes
    def test_item_total_updates_when_quantity_changes(self):
        item = OrderItem.objects.create(
            order=self.order, record=self.record, quantity=1)
        self.assertEqual(item.item_total, Decimal("10.00"))

        item.quantity = 4
        item.save()
        self.assertEqual(item.item_total, Decimal("40.00"))

    # Tests that quantity is not able to be negative
    def test_quantity_cannot_be_negative(self):
        item = OrderItem(order=self.order, record=self.record, quantity=-1)
        with self.assertRaises(ValidationError):
            item.full_clean()

    # Tests quantity can't exceed 9
    def test_quantity_cannot_exceed_max(self):
        item = OrderItem(order=self.order, record=self.record, quantity=10)
        with self.assertRaises(ValidationError):
            item.full_clean()
