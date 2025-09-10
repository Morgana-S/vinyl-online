from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from .models import Order, OrderItem
from records.models import Artist, Genre, Record


class UpdateOnSaveSignalTest(TestCase):
    """
    TestCase for the update_on_save signal.
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
        self.record2 = Record.objects.create(
            title='Test Record',
            slug='test-record-2',
            artist=self.artist,
            price=Decimal('20.00'),
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

    # Creating an order item should update the total
    def test_signal_updates_order_total_on_item_create(self):
        OrderItem.objects.create(
            order=self.order, record=self.record, quantity=2)
        self.order.refresh_from_db()
        self.assertEqual(self.order.subtotal_cost, Decimal("20.00"))
        self.assertEqual(self.order.grand_total_cost,
                         self.order.subtotal_cost + self.order.delivery_cost)

    # Updating an order updates total
    def test_signal_updates_order_total_on_item_update(self):
        item = OrderItem.objects.create(
            order=self.order, record=self.record, quantity=1)
        self.order.refresh_from_db()
        self.assertEqual(self.order.subtotal_cost, Decimal("10.00"))

        # Update quantity
        item.quantity = 3
        item.save()
        self.order.refresh_from_db()
        self.assertEqual(self.order.subtotal_cost, Decimal("30.00"))

    # Tests update is correct when multiple items are introduced
    def test_signal_with_multiple_items(self):
        OrderItem.objects.create(
            order=self.order, record=self.record, quantity=2)
        OrderItem.objects.create(
            order=self.order, record=self.record2, quantity=1)
        self.order.refresh_from_db()
        self.assertEqual(self.order.subtotal_cost, Decimal("40.00"))
        self.assertEqual(self.order.grand_total_cost,
                         self.order.subtotal_cost + self.order.delivery_cost)


class UpdateOnDeleteSignalTest(TestCase):
    """
    TestCase for the update_on_delete signal.
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
        self.record2 = Record.objects.create(
            title='Test Record',
            slug='test-record-2',
            artist=self.artist,
            price=Decimal('20.00'),
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

    # Tests deleting an item updates total
    def test_signal_updates_order_total_on_item_delete(self):
        item = OrderItem.objects.create(
            order=self.order, record=self.record, quantity=2)
        self.order.refresh_from_db()
        self.assertEqual(self.order.subtotal_cost, Decimal("20.00"))

        # Delete the item
        item.delete()
        self.order.refresh_from_db()

        # Totals should reset to 0
        self.assertEqual(self.order.subtotal_cost, Decimal("0.00"))
        self.assertEqual(self.order.grand_total_cost, Decimal("0.00"))

    # Tests that totals update with multiple items
    def test_signal_with_multiple_items_and_delete_one(self):
        item1 = OrderItem.objects.create(
            order=self.order, record=self.record, quantity=1)
        item2 = OrderItem.objects.create(
            order=self.order, record=self.record2, quantity=2)
        self.order.refresh_from_db()
        self.assertEqual(self.order.subtotal_cost, Decimal("50.00"))

        # Delete item1
        item1.delete()
        self.order.refresh_from_db()

        # Only item2 should remain
        self.assertEqual(self.order.subtotal_cost, Decimal("40.00"))
        self.assertEqual(self.order.grand_total_cost,
                         self.order.subtotal_cost + self.order.delivery_cost)
