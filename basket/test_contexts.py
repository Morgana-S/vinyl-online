from decimal import Decimal
from django.test import TestCase, RequestFactory
from django.conf import settings
from records.models import Record, Artist
from .contexts import basket_contents


class BasketContentsContextProcessorTest(TestCase):
    """
    TestCase for the basket_contents context processor.
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.artist = Artist.objects.create(
            name='Test Artist',
            slug='test-artist'
        )
        self.record = Record.objects.create(
            title='Test Record',
            slug='test-record',
            artist=self.artist,
            price=Decimal('10.00'),
            quantity=5
        )
        self.record2 = Record.objects.create(
            title='Test Record 2',
            slug='test-record-2',
            artist=self.artist,
            price=Decimal('15.00'),
            quantity=5
        )

    # Tests information with an empty basket
    def test_empty_basket(self):
        request = self.factory.get('/')
        request.session = {'basket': {}}

        context = basket_contents(request)

        self.assertEqual(context['basket_items'], [])
        self.assertEqual(context['record_count'], 0)
        self.assertEqual(context['subtotal_cost'], Decimal('0.00'))
        self.assertEqual(context['delivery_cost'], Decimal('0.00'))
        self.assertEqual(context['grand_total'], Decimal('0.00'))

    # Tests basket with multiple items
    def test_basket_with_items(self):
        request = self.factory.get('/')
        request.session = {
            'basket': {
                str(self.record.id): 2,
                str(self.record2.id): 1
            }
        }

        context = basket_contents(request)

        # Test basket items
        self.assertEqual(len(context['basket_items']), 2)
        self.assertEqual(context['record_count'], 3)
        expected_subtotal = (self.record.price * 2 + self.record2.price * 1)
        self.assertEqual(context['subtotal_cost'], expected_subtotal)

        # Delivery cost logic
        if expected_subtotal < Decimal(settings.FREE_DELIVERY_THRESHOLD):
            expected_delivery = expected_subtotal * \
                Decimal(settings.STANDARD_DELIVERY_MODIFIER)
        else:
            expected_delivery = Decimal('0.00')

        self.assertEqual(context['delivery_cost'], expected_delivery)
        self.assertEqual(context['grand_total'],
                         expected_subtotal + expected_delivery)

    # Tests basket with non-existent record
    def test_basket_with_nonexistent_record(self):
        request = self.factory.get('/')
        request.session = {'basket': {'9999': 1}}

        context = basket_contents(request)

        self.assertEqual(context['basket_items'], [])
        self.assertEqual(context['record_count'], 0)
        self.assertEqual(context['subtotal_cost'], Decimal('0.00'))

