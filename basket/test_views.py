from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from records.models import Record, Artist
import json
# Create your tests here.


class ViewBasketTest(TestCase):
    """
    TestCase for the view_basket view.
    """

    def setUp(self):
        self.artist = Artist.objects.create(
            name='Test Artist',
            slug='test-artist'
        )
        for i in range(10):
            Record.objects.create(
                title=f'Record {i}',
                slug=f'test-record-{i}',
                artist=self.artist,
                price=Decimal('10.00'),
                quantity=5
            )
        self.client = Client()

    # Tests the basket renders the correct template
    def test_view_basket_renders_correct_template(self):
        response = self.client.get(reverse('view_basket'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/view_basket.html')
        self.assertIn('suggested_records', response.context)
        self.assertLessEqual(len(response.context['suggested_records']), 5)


class AddToBasketAsyncTest(TestCase):
    """
    TestCase for the Async add_to_basket view.
    """
    def setUp(self):
        self.artist = Artist.objects.create(
            name='Test Artist',
            slug='test-artist'
        )
        self.record = Record.objects.create(
                title='Record',
                slug='test-record',
                artist=self.artist,
                price=Decimal('10.00'),
                quantity=50
            )
        self.client = Client()

    # Tests whether items are successfully added to basket
    def test_add_to_basket_successful(self):
        response = self.client.post(
            reverse('add_to_basket'),
            {'record_id': self.record.id, 'quantity': 2},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(response.status_code, 200)

        # Check session updated
        session_basket = self.client.session['basket']
        self.assertEqual(session_basket[str(self.record.id)], 2)

        # Check JSON response
        data = json.loads(response.content)
        self.assertEqual(data['toast_header'], 'Added to Basket')
        self.assertEqual(
            data['toast_message'],
            f'Added 2 x {self.record.title} to your basket!'
        )
        self.assertEqual(data['basket_count'], 2)

    # Test to ensure no more than 9 of the same record can be added
    def test_add_to_basket_max_quantity(self):
        session = self.client.session
        session['basket'] = {str(self.record.id): 8}
        session.save()

        response = self.client.post(
            reverse('add_to_basket'),
            {'record_id': self.record.id, 'quantity': 5},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(response.status_code, 200)

        # Check that quantity is capped at 9
        session_basket = self.client.session['basket']
        self.assertEqual(session_basket[str(self.record.id)], 9)

        # Check JSON response
        data = json.loads(response.content)
        self.assertEqual(data['toast_header'], 'Maximum Quantity Reached')
        self.assertIn('Unable to add record', data['toast_message'])
        self.assertEqual(data['basket_count'], 9)


class RemoveFromBasketTest(TestCase):
    """
    TestCase for remove_from_basket view.
    """

    def setUp(self):
        self.artist = Artist.objects.create(
            name='Test Artist',
            slug='test-artist'
        )
        self.record1 = Record.objects.create(
            title='Record',
            slug='test-record',
            artist=self.artist,
            price=Decimal('10.00'),
            quantity=50
        )
        self.record2 = Record.objects.create(
            title='Record 2',
            slug='test-record-2',
            artist=self.artist,
            price=Decimal('12.00'),
            quantity=50
        )
        self.client = Client()

    # Tests removing a record from the basket
    def test_remove_record_from_basket(self):
        session = self.client.session
        session['basket'] = {
            str(self.record1.id): 2,
            str(self.record2.id): 1
        }
        session.save()

        # Remove record1
        response = self.client.get(
            reverse('remove_basket_item', args=[self.record1.id])
        )

        # Check redirect
        self.assertRedirects(response, reverse('view_basket'))

        # Check that record1 is removed, record2 still present
        updated_basket = self.client.session['basket']
        self.assertNotIn(str(self.record1.id), updated_basket)
        self.assertIn(str(self.record2.id), updated_basket)
        self.assertEqual(updated_basket[str(self.record2.id)], 1)

    # Tests removing an item that isn't in the basket
    def test_remove_nonexistent_record(self):
        session = self.client.session
        session['basket'] = {}
        session.save()

        # Attempt to remove a record that isn't in the basket
        response = self.client.get(
            reverse('remove_basket_item', args=[self.record1.id])
        )

        # Should still redirect
        self.assertRedirects(response, reverse('view_basket'))

        # Basket remains empty
        updated_basket = self.client.session['basket']
        self.assertEqual(updated_basket, {})


class UpdateBasketQuantityView(TestCase):
    """
    TestCase for update_basket_quantity_view.
    """

    def setUp(self):
        self.client = Client()
        self.url = reverse('update_basket')
        self.basket_session = {
            '1': 2,
            '2': 5
        }

    # Tests updating the basket quantities
    def test_update_basket_quantities(self):
        # Initialize session basket
        session = self.client.session
        session['basket'] = self.basket_session
        session.save()

        # Post new quantities
        response = self.client.post(self.url, {
            'quantity_1': 4,  # increase
            'quantity_2': 0,  # remove
            'quantity_3': 10,  # capped at 9
            'quantity_4': 'invalid'  # invalid, set to 1
        })

        # Check redirection
        self.assertRedirects(response, reverse('view_basket'))

        # Check session basket updated correctly
        session = self.client.session
        expected_basket = {
            '1': 4,      # updated
            '3': 9,      # capped
            '4': 1       # invalid parsed to 1
            # record2 removed because quantity=0
        }
        self.assertEqual(session['basket'], expected_basket)
