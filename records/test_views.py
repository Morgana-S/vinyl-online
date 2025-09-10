from decimal import Decimal
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from unittest.mock import patch
import json
from checkout.models import Order, OrderItem
from .models import Artist, Record, Genre, Review


class IndexViewTest(TestCase):
    """
    TestCase for the index_view
    """

    def setUp(self):
        # Create a genre
        self.pop_genre = Genre.objects.create(
            name='Pop',
            color='#FFFFFF',
            description='Popular music'
        )

        # Create an artist
        self.artist = Artist.objects.create(name='Test Artist')

        # Create 6 records, some with 'Pop' genre
        for i in range(6):
            record = Record.objects.create(
                title=f'Record {i}',
                artist=self.artist,
                size='12"',
                rpm='33',
                price=10.00,
                quantity=5,
                hidden=False
            )
            if i < 3:
                record.genre.add(self.pop_genre)

    # Should return 200 if url is correct
    def test_index_view_status_code(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    # Tests correct template in use
    def test_index_view_template_used(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'records/index.html')

    # Tests the view contexts
    def test_index_view_context(self):
        response = self.client.get(reverse('index'))
        self.assertIn('latest_releases', response.context)
        self.assertIn('featured_genre', response.context)
        self.assertIn('featured_genre_records', response.context)

        # latest_releases should be 5 most recent non-hidden records
        self.assertEqual(len(response.context['latest_releases']), 5)

        # featured_genre should be 'Pop'
        self.assertEqual(response.context['featured_genre'], 'Pop')

        # featured_genre_records should only include records with Pop genre
        for record in response.context['featured_genre_records']:
            self.assertIn(self.pop_genre, record.genre.all())


class SearchRecordsViewTest(TestCase):
    """
    TestCase for the search_records view.
    """

    def setUp(self):
        # Create artists
        self.artist1 = Artist.objects.create(name='The Beatles')
        self.artist2 = Artist.objects.create(name='Queen')
        self.artist3 = Artist.objects.create(name='Metallica')

        # Create an artist with no matching search term
        self.artist4 = Artist.objects.create(name='Nirvana')

        # Create records
        self.record1 = Record.objects.create(
            title='Abbey Road',
            artist=self.artist1,
            size='12"',
            rpm='33',
            price=15.00,
            quantity=5,
            hidden=False
        )
        self.record2 = Record.objects.create(
            title='A Night at the Opera',
            artist=self.artist2,
            size='12"',
            rpm='33',
            price=12.00,
            quantity=3,
            hidden=False
        )
        self.record3 = Record.objects.create(
            title='Master of Puppets',
            artist=self.artist3,
            size='12"',
            rpm='33',
            price=14.00,
            quantity=2,
            hidden=True  # hidden records should be excluded
        )

    # Status code returns 200
    def test_search_view_status_code(self):
        response = self.client.get(reverse('search') + '?q=Queen')
        self.assertEqual(response.status_code, 200)

    # Correct Template is used
    def test_search_view_template_used(self):
        response = self.client.get(reverse('search') + '?q=Queen')
        self.assertTemplateUsed(response, 'records/search.html')

    # Search query is fed to context
    def test_search_view_query_context(self):
        response = self.client.get(reverse('search') + '?q=Queen')
        self.assertEqual(response.context['query'], 'Queen')

    # Searching for a specific artist
    def test_search_view_artist_results(self):
        response = self.client.get(reverse('search') + '?q=Queen')
        # Should include only Queen
        artist_names = [
            artist.name for artist in response.context['artists_results']]
        self.assertIn('Queen', artist_names)
        self.assertNotIn('The Beatles', artist_names)
        self.assertNotIn('Metallica', artist_names)

    # Searching for specific records
    def test_search_view_record_results(self):
        response = self.client.get(reverse('search') + '?q=Abbey')
        # Should include Abbey Road
        record_titles = [
            record.title for record in response.context['records_results']]
        self.assertIn('Abbey Road', record_titles)
        # Hidden records should be excluded
        self.assertNotIn('Master of Puppets', record_titles)


class SearchRecordsAsyncViewTest(TestCase):
    """
    TestCase for Async search view.
    """

    def setUp(self):
        # Set up test client
        self.client = Client()

        # Create test artists
        self.artist1 = Artist.objects.create(name="Queen")
        self.artist2 = Artist.objects.create(name="The Beatles")

        # Create test records
        self.record1 = Record.objects.create(
            title="Bohemian Rhapsody",
            artist=self.artist1,
            size='12"',
            rpm='33',
            price=10.99,
            quantity=5,
            hidden=False
        )
        self.record2 = Record.objects.create(
            title="Hey Jude",
            artist=self.artist2,
            size='12"',
            rpm='33',
            price=9.99,
            quantity=3,
            hidden=False
        )

    # Test that query returns both records and artists with query name
    def test_search_records_async_returns_records_and_artists(self):
        url = reverse('async_search')
        response = self.client.get(url, {'q': 'Queen'})

        # Assert that the response is JSON
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Expecting at least one record and/or artist in the results
        self.assertTrue(any(item['type'] == 'record' for item in data))
        self.assertTrue(any(item['type'] == 'artist' for item in data))

        # Check that the returned artist is correct
        artist_names = [item['name']
                        for item in data if item['type'] == 'artist']
        self.assertIn("Queen", artist_names)

        # Check that the returned record belongs to the artist
        record_titles = [item['name']
                         for item in data if item['type'] == 'record']
        self.assertIn("Bohemian Rhapsody", record_titles)

    # Test that results are empty
    def test_search_records_async_empty_query(self):
        url = reverse('async_search')
        response = self.client.get(url, {'q': ''})

        # Should return an empty JSON array
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data, [])


class RecordDetailViewTest(TestCase):
    """
    TestCase for record detail view.
    """

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username='testuser',
            password='password'
        )

        # Create an artist
        self.artist = Artist.objects.create(
            name='Test Artist',
            slug='test-artist'
        )

        # Create a record
        self.record = Record.objects.create(
            title='Test Record',
            artist=self.artist,
            price=Decimal('10.00'),
            slug='test-record',
            quantity='5',
            hidden=False,
        )

        # Create a review authored by the user
        self.review = Review.objects.create(
            author=self.user,
            record=self.record,
            delivery_rating=5,
            quality_rating=5,
            record_rating=5,
            is_approved=True
        )

        # Create an order with this record for the user
        self.order = Order.objects.create(
            user=self.user,
            status='delivered',
            full_name='Test User',
            address_line1='123 Test St',
            postcode='AB12 3CD',
            phone_number='+441234567890',
            email='test@example.com',
            subtotal_cost=Decimal('10.00'),
            delivery_cost=Decimal('2.00'),
            grand_total_cost=Decimal('12.00'),
            stripe_pid='testpid123'
        )
        OrderItem.objects.create(
            order=self.order,
            record=self.record,
            quantity=1
        )

    # Tests authenticated user review details
    def test_authenticated_user_review_flags(self):
        # Log in the user
        self.client.login(username='testuser', password='password')

        url = reverse('record_detail', args=[self.record.slug])
        response = self.client.get(url)

        # Check that the record is in context
        self.assertEqual(response.context['record'], self.record)

        # Check that is_reviewable is True because user has a delivered order
        self.assertTrue(response.context['is_reviewable'])

        # Check that has_reviewed is True because user authored a review
        self.assertTrue(response.context['has_reviewed'])

        # Access reviews from context to check is_deletable
        reviews_in_context = response.context['reviews']
        review = next(r for r in reviews_in_context if r.author == self.user)
        self.assertTrue(review.is_deletable)

    # Tests anonymous user review details
    def test_anonymous_user_flags(self):
        url = reverse('record_detail', args=[self.record.slug])
        response = self.client.get(url)

        # Anonymous user cannot review
        self.assertFalse(response.context['is_reviewable'])
        self.assertFalse(response.context['has_reviewed'])

        # Reviews should exist but is_deletable is False
        reviews_in_context = response.context['reviews']
        review = reviews_in_context[0]
        self.assertFalse(review.is_deletable)

    # Tests pagination
    def test_pagination(self):
        for i in range(5):
            Review.objects.create(
                author=self.user,
                record=self.record,
                delivery_rating=5,
                quality_rating=5,
                record_rating=5
            )

        url = reverse('record_detail', args=[self.record.slug])

        # Test page 1
        response = self.client.get(url + '?page=1')
        self.assertEqual(len(response.context['reviews_page']), 3)
        self.assertTrue(response.context['reviews_page'].has_next())
        self.assertFalse(response.context['reviews_page'].has_previous())

        # Test page 2
        response = self.client.get(url + '?page=2')
        self.assertEqual(len(response.context['reviews_page']), 3)
        self.assertFalse(response.context['reviews_page'].has_next())
        self.assertTrue(response.context['reviews_page'].has_previous())


class AddRecordViewTest(TestCase):
    """
    TestCase for add_record_view.
    """

    def setUp(self):
        self.client = Client()
        self.url = reverse('add_record')

        # Regular user
        self.user = User.objects.create_user(
            username='regular',
            password='password',
            is_staff=False
        )

        # Staff user
        self.staff_user = User.objects.create_user(
            username='staff',
            password='password',
            is_staff=True
        )

        self.artist = Artist.objects.create(
            name='Test Artist',
            slug='test-artist'
        )

    # Tests that non-staff users are redirected
    def test_redirect_if_not_staff(self):
        self.client.login(username='regular', password='password')
        response = self.client.get(self.url, follow=True)

        self.assertRedirects(response, reverse('index'))
        messages = list(response.context['messages'])
        self.assertTrue(any("staff" in str(m) for m in messages))

    # Test staff users can see form on GET request
    def test_get_staff_user_sees_form(self):
        self.client.login(username='staff', password='password')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'records/create_record.html')
        self.assertIn('form', response.context)
        self.assertIn('formset', response.context)

    # Test valid POST request creates a record
    def test_post_creates_record(self):
        self.client.login(username='staff', password='password')

        self.image = SimpleUploadedFile(
            name='test.jpg',
            content=b'file_content',
            content_type='image/jpeg'
        )

        data = {
            "title": "Test Record",
            "slug": "test-record",
            "artist": self.artist.id,
            "price": 10.00,
            "quantity": 10,
            "size": '7"',
            "rpm": "33",
            "hidden": False,

            "recordimage_set-TOTAL_FORMS": "0",
            "recordimage_set-INITIAL_FORMS": "0",
            "recordimage_set-MIN_NUM_FORMS": "0",
            "recordimage_set-MAX_NUM_FORMS": "5",
        }

        post_data = {**data}

        response = self.client.post(
            self.url, post_data, follow=True)

        # should redirect to index on success
        self.assertRedirects(response, reverse('index'))

        # record created
        self.assertTrue(Record.objects.filter(title="Test Record").exists())

        messages = list(response.context['messages'])
        self.assertTrue(any("created" in str(m) for m in messages))


class EditRecordViewTest(TestCase):
    """
    TestCase for edit_record_view.
    """

    def setUp(self):
        self.client = Client()
        self.url = reverse('add_record')

        # Regular user
        self.user = User.objects.create_user(
            username='regular',
            password='password',
            is_staff=False
        )

        # Staff user
        self.staff_user = User.objects.create_user(
            username='staff',
            password='password',
            is_staff=True
        )

        self.artist = Artist.objects.create(
            name='Test Artist',
            slug='test-artist'
        )

        self.record = Record.objects.create(
            title='Test Record',
            slug='test-record',
            artist=self.artist,
            price=10.00,
            quantity=5,
            size='7"',
            rpm='33'
        )
        self.url = reverse('edit_record', args=[self.record.slug])

    # Tests that the view shows the form on a GET request for staff
    def test_get_edit_record_view_as_staff(self):
        self.client.login(username='staff', password='password')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'records/edit_record.html')
        self.assertIn('form', response.context)
        self.assertIn('formset', response.context)
        self.assertEqual(response.context['form'].instance, self.record)

    # Tests that the view redirects as a regular user
    def test_redirect_if_not_staff(self):
        self.client.login(username='regular', password='password')
        response = self.client.get(self.url, follow=True)

        self.assertRedirects(response, reverse('record_detail',
                                               args=[self.record.slug]))
        messages = list(response.context['messages'])
        self.assertTrue(any("staff" in str(m) for m in messages))

    # Tests that record details are updated on post
    def test_post_valid_edit_updates_record(self):
        self.client.login(username='staff', password='password')

        data = {
            'title': 'Updated Record',
            'slug': self.record.slug,
            'artist': self.artist.id,
            'price': 12.50,
            'quantity': 10,
            'size': '12"',
            'rpm': '45',
            'hidden': False,
        }

        response = self.client.post(self.url, data, follow=True)

        # Should redirect to record detail on success
        self.assertRedirects(response, reverse(
            'record_detail', args=[self.record.slug]))

        # Record should be updated
        self.record.refresh_from_db()
        self.assertEqual(self.record.title, 'Updated Record')
        self.assertEqual(self.record.price, 12.50)
        self.assertEqual(self.record.quantity, 10)
        self.assertEqual(self.record.size, '12"')
        self.assertEqual(self.record.rpm, '45')

        # Success message
        messages = list(response.context['messages'])
        self.assertTrue(any("successfully edited" in str(m) for m in messages))


class DeleteRecordViewTest(TestCase):
    """
    TestCase for delete_record_view.
    """

    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username='staff', password='password', is_staff=True
        )
        self.non_staff_user = User.objects.create_user(
            username='nonstaff', password='password', is_staff=False
        )
        self.artist = Artist.objects.create(
            name='Test Artist', slug='test-artist')
        self.record = Record.objects.create(
            title='Record To Delete',
            slug='record-to-delete',
            artist=self.artist,
            price=10.00,
            quantity=5,
            size='7"',
            rpm='33'
        )
        self.url = reverse('delete_record', args=[self.record.slug])

    # Tests staff can delete record
    def test_staff_can_delete_record(self):
        self.client.login(username='staff', password='password')
        response = self.client.post(self.url, follow=True)

        self.assertRedirects(response, reverse('index'))
        self.assertFalse(Record.objects.filter(
            slug='record-to-delete').exists())

        messages = list(response.context['messages'])
        self.assertTrue(any("deleted" in str(m) for m in messages))

    # Tests staff on a GET request are redirected
    def test_staff_get_redirects_to_detail(self):
        self.client.login(username='staff', password='password')
        response = self.client.get(self.url, follow=True)

        self.assertRedirects(response, reverse(
            'record_detail', args=[self.record.slug]))

        self.assertTrue(Record.objects.filter(
            slug='record-to-delete').exists())

    # Tests non-staff users are not able to delete records
    def test_non_staff_cannot_delete_record(self):
        self.client.login(username='nonstaff', password='password')
        response = self.client.post(self.url, follow=True)

        self.assertRedirects(response, reverse(
            'record_detail', args=[self.record.slug]))

        self.assertTrue(Record.objects.filter(
            slug='record-to-delete').exists())

        messages = list(response.context['messages'])
        self.assertTrue(any("member of staff" in str(m) for m in messages))


class ArtistDetailViewTest(TestCase):
    """
    TestCase for artist_detail_view.
    """

    def setUp(self):
        self.client = Client()

        # Create an artist
        self.artist = Artist.objects.create(
            name='Test Artist',
            slug='test-artist'
        )

        self.visible_records = []
        for i in range(6):
            record = Record.objects.create(
                title=f'Visible Record {i+1}',
                slug=f'visible-record-{i+1}',
                artist=self.artist,
                price=Decimal('10.00'),
                quantity=5,
                size='7"',
                rpm='33',
                hidden=False
            )
            self.visible_records.append(record)

        self.hidden_record = Record.objects.create(
            title='Hidden Record',
            slug='hidden-record',
            artist=self.artist,
            price=Decimal('12.00'),
            quantity=5,
            size='7"',
            rpm='33',
            hidden=True
        )

        self.url = reverse('artist_detail', args=[self.artist.slug])

    # Tests response code, correct template, context
    def test_artist_detail_view_status_and_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'records/artist_detail.html')
        self.assertIn('artist', response.context)
        self.assertIn('record_results', response.context)
        self.assertEqual(response.context['artist'], self.artist)

    # Tests hidden records are not displayed
    def test_only_non_hidden_records_displayed(self):
        response = self.client.get(self.url)
        record_results = response.context['record_results'].object_list
        for record in record_results:
            self.assertFalse(record.hidden)
        self.assertNotIn(self.hidden_record, record_results)

    # Tests pagination
    def test_pagination_limits(self):
        for i in range(2):
            Record.objects.create(
                title=f'Extra Record {i+1}',
                slug=f'extra-record-{i+1}',
                artist=self.artist,
                price=Decimal('10.00'),
                quantity=5,
                size='7"',
                rpm='33',
                hidden=False
            )
        response = self.client.get(self.url)
        record_results = response.context['record_results']
        # There should be 6 records on first page
        self.assertEqual(len(record_results), 6)
        # Second page should exist
        response_page2 = self.client.get(self.url + '?page=2')
        record_results_page2 = response_page2.context['record_results']
        self.assertTrue(record_results_page2.has_other_pages())


class AddArtistViewTest(TestCase):
    """
    TestCase for the add_artist_view.
    """

    def setUp(self):
        self.client = Client()
        self.url = reverse('add_artist')
        self.staff_user = User.objects.create_user(
            username='staff',
            password='password',
            is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='user',
            password='password',
            is_staff=False
        )

    # Tests a staff member can add an artist
    def test_staff_can_add_artist(self):
        self.client.login(username='staff', password='password')
        data = {
            'name': 'Test Artist',
            'slug': 'test-artist',
            'bio': 'An amazing artist'
        }

        response = self.client.post(self.url, data, follow=True)

        self.assertRedirects(response, reverse('index'))
        self.assertTrue(Artist.objects.filter(slug='test-artist').exists())

        messages = list(response.context['messages'])
        self.assertTrue(any("successfully" in str(m) for m in messages))

    # Tests non-staff users are redirected
    def test_non_staff_user_redirected(self):
        self.client.login(username='user', password='password')

        response = self.client.get(self.url, follow=True)

        self.assertRedirects(response, reverse('index'))

        messages = list(response.context['messages'])
        self.assertTrue(any("must be a member of staff" in str(m)
                        for m in messages))


class EditArtistViewTest(TestCase):
    """
    TestCase for edit_artist_view.
    """

    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username='staff',
            password='password',
            is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='user',
            password='password',
            is_staff=False
        )
        self.artist = Artist.objects.create(
            name='Original Artist',
            slug='original-artist',
            bio='Original bio'
        )
        self.url = reverse('edit_artist', kwargs={
                           'artist_slug': self.artist.slug})

    # Tests staff can edit the artist
    def test_staff_can_edit_artist(self):
        self.client.login(username='staff', password='password')

        data = {
            'name': 'Updated Artist',
            'slug': 'original-artist',
            'bio': 'Updated bio'
        }

        response = self.client.post(self.url, data, follow=True)

        self.assertRedirects(response, reverse(
            'artist_detail', kwargs={'artist_slug': 'original-artist'}))

        self.artist.refresh_from_db()
        self.assertEqual(self.artist.name, 'Updated Artist')
        self.assertEqual(self.artist.bio, 'Updated bio')

        messages = list(response.context['messages'])
        self.assertTrue(any("successfully edited" in str(m) for m in messages))

    # Tests non-staff users are redirected
    def test_non_staff_redirected(self):
        self.client.login(username='user', password='password')

        response = self.client.get(self.url, follow=True)

        self.assertRedirects(response, reverse('index'))

        messages = list(response.context['messages'])
        self.assertTrue(any("must be a member of staff" in str(m)
                        for m in messages))


class DeleteArtistViewTest(TestCase):
    """
    TestCase for the delete_artist_view.
    """

    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username='staff',
            password='password',
            is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='user',
            password='password',
            is_staff=False
        )
        self.artist = Artist.objects.create(
            name='Test Artist',
            slug='test-artist',
            bio='Test bio'
        )
        self.url = reverse('delete_artist', kwargs={
                           'artist_slug': self.artist.slug})

    # Tests staff can delete artist
    def test_staff_can_delete_artist(self):
        self.client.login(username='staff', password='password')

        response = self.client.post(self.url, follow=True)

        self.assertRedirects(response, reverse('index'))

        with self.assertRaises(Artist.DoesNotExist):
            Artist.objects.get(slug='test-artist')

        messages = list(response.context['messages'])
        self.assertTrue(any("has now been deleted" in str(m)
                        for m in messages))

    # Tests GET request redirects to artist detail
    def test_staff_get_request_redirects_to_artist_detail(self):
        self.client.login(username='staff', password='password')

        response = self.client.get(self.url, follow=True)

        self.assertRedirects(response, reverse(
            'artist_detail', kwargs={'artist_slug': 'test-artist'}))

        self.assertTrue(Artist.objects.filter(slug='test-artist').exists())

    # Tests that non-staff are not able to delete artist
    def test_non_staff_user_cannot_delete(self):
        self.client.login(username='user', password='password')

        response = self.client.post(self.url, follow=True)

        self.assertRedirects(response, reverse('index'))

        self.assertTrue(Artist.objects.filter(slug='test-artist').exists())

        messages = list(response.context['messages'])
        self.assertTrue(any("must be a member of staff" in str(m)
                        for m in messages))


class BrowseByGenreTestView(TestCase):
    """
    TestCase for the browse_by_genre view.
    """

    def setUp(self):
        self.client = Client()
        self.genre = Genre.objects.create(
            name='Pop',
            slug='pop',
            color='#FFFFFF',
            description='Pop genre'
        )
        self.artist = Artist.objects.create(
            name='Test Artist',
            slug='test-artist'
        )
        self.records = []
        for i in range(20):
            record = Record.objects.create(
                title=f'Record {i}',
                slug=f'record-{i}',
                artist=self.artist,
                price=10.00 + i,
                quantity=5,
                hidden=False,
            )
            record.save()
            record.genre.add(self.genre)
            self.records.append(record)

        self.url = reverse('browse_by_genre', kwargs={
                           'genre_name': self.genre.slug})

    # Tests that genre page renders with status code, template, context
    def test_genre_page_renders_with_records(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'records/browse_by_genre.html')
        self.assertEqual(response.context['genre'], self.genre)

        records_in_context = response.context['records_results'].object_list
        self.assertTrue(all(r.genre.filter(pk=self.genre.pk).exists()
                        for r in records_in_context))

    # Tests pagination
    def test_pagination_works(self):
        response = self.client.get(self.url)
        records_results = response.context['records_results']
        self.assertEqual(Record.objects.filter(
            genre=self.genre, hidden=False).count(), 20)
        self.assertEqual(records_results.paginator.num_pages,
                         2)
        self.assertEqual(len(records_results.object_list),
                         16)

        # Test second page
        response_page2 = self.client.get(self.url + '?records_page=2')
        records_results_page2 = response_page2.context['records_results']
        self.assertEqual(
            len(records_results_page2.object_list), 4)

    # Test invalid genre returns 404
    def test_invalid_genre_returns_404(self):
        invalid_url = reverse('browse_by_genre', kwargs={
                              'genre_name': 'nonexistent'})
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 404)

    # Tests records can be sorted by title descending (Z-A)
    def test_sorting_by_title_desc(self):
        response = self.client.get(self.url + '?sort_record=title_desc')
        records_results = response.context['records_results'].object_list
        titles = [r.title for r in records_results]
        self.assertEqual(titles, sorted(titles, reverse=True))


class AllRecordsViewTest(TestCase):
    """
    TestCase for all_records_view.
    """

    def setUp(self):
        self.client = Client()
        self.genre = Genre.objects.create(
            name='Pop',
            slug='pop',
            color='#FFFFFF',
            description='Pop genre'
        )
        self.artist = Artist.objects.create(
            name='Test Artist',
            slug='test-artist'
        )
        self.records = []
        for i in range(20):
            record = Record.objects.create(
                title=f'Record {i}',
                slug=f'record-{i}',
                artist=self.artist,
                price=10.00 + i,
                quantity=5,
                hidden=False,
            )
            record.save()
            record.genre.add(self.genre)
            self.records.append(record)
        self.url = reverse('all_records')

    # Tests status code, context, template
    def test_all_records_renders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'records/all_records.html')
        response_titles = [r.title for r in response.context['records']]
        expected_titles = sorted([r.title for r in self.records])
        self.assertEqual(response_titles, expected_titles)

    # Tests pagination
    def test_pagination(self):
        response = self.client.get(self.url)
        records_results = response.context['records_results']
        self.assertEqual(records_results.paginator.num_pages, 2)
        self.assertEqual(len(records_results.object_list), 16)

        # Second page
        response_page2 = self.client.get(self.url + '?records_page=2')
        records_results_page2 = response_page2.context['records_results']
        # remaining records
        self.assertEqual(len(records_results_page2.object_list), 4)

    # Tests sorting by Z-A
    def test_sorting_by_title_desc(self):
        response = self.client.get(self.url + '?sort_record=title_desc')
        records_results = response.context['records_results'].object_list
        titles = [r.title for r in records_results]
        self.assertEqual(titles, sorted(titles, reverse=True))

    # Tests sorting by price lowest to high
    def test_sorting_by_price_asc(self):
        """Test sorting by price ascending"""
        response = self.client.get(self.url + '?sort_record=price_asc')
        records_results = response.context['records_results'].object_list
        prices = [r.price for r in records_results]
        self.assertEqual(prices, sorted(prices))


class LatestReleasesViewTest(TestCase):
    """
    TestCase for latest_releases_view.
    """

    def setUp(self):
        self.client = Client()
        self.artist = Artist.objects.create(
            name="Test Artist", slug="test-artist")
        self.records = []
        for i in range(20):
            record = Record.objects.create(
                title=f"Record {i}",
                slug=f"record-{i}",
                artist=self.artist,
                price=10.0 + i,
                quantity=5,
                hidden=False
            )
            self.records.append(record)

        self.url = reverse('latest_releases')

    # Test template, status code, context
    def test_latest_releases_view_renders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'records/latest_records.html')
        self.assertIn('records', response.context)

    # Tests most recently created records are the ones returned
    def test_latest_releases_returns_16_most_recent(self):
        response = self.client.get(self.url)
        records_in_context = list(response.context['records'])
        self.assertEqual(len(records_in_context), 16)
        # Ensure the records are ordered by newest first
        expected_order = sorted(
            self.records, key=lambda r: r.created_at, reverse=True)[:16]
        self.assertEqual(records_in_context, expected_order)

    # Tests hidden records are excluded
    def test_hidden_records_are_excluded(self):
        self.records[0].hidden = True
        self.records[0].save()
        response = self.client.get(self.url)
        records_in_context = list(response.context['records'])
        self.assertNotIn(self.records[0], records_in_context)


class AnalyticsPageViewTest(TestCase):
    """
    TestCase for the analytics_page_view.
    """

    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username='staff', email='staff@example.com',
            password='password', is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='user', email='user@example.com', password='password'
        )
        self.artist = Artist.objects.create(
            name='Test Artist', slug='test-artist')
        self.records = []
        for i in range(15):
            record = Record.objects.create(
                title=f'Record {i}',
                slug=f'record-{i}',
                artist=self.artist,
                price=Decimal('10.00'),
                quantity=i,
                hidden=False
            )
            self.records.append(record)
        order = Order.objects.create(
            user=self.regular_user,
            full_name='User',
            email='user@example.com',
            subtotal_cost=Decimal('50.00'),
            delivery_cost=Decimal('5.00'),
            grand_total_cost=Decimal('55.00'),
            stripe_pid='pi_test'
        )
        for record in self.records[:5]:
            OrderItem.objects.create(
                order=order,
                record=record,
                quantity=record.quantity or 1
            )

        self.url = reverse('analytics')

    # Tests non-staff are redirected
    def test_non_staff_redirected(self):
        self.client.login(username='user', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    # Tests staff can access analytics page, context, template
    def test_staff_can_access_analytics(self):
        self.client.login(username='staff', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'records/analytics.html')
        self.assertIn('popular_records', response.context)
        self.assertIn('weekly_sales_data', response.context)
        self.assertIn('low_stock_records', response.context)

    # Tests that the analytics data is correct
    def test_analytics_data_correct(self):
        self.client.login(username='staff', password='password')
        response = self.client.get(self.url)
        popular_records = response.context['popular_records']
        low_stock_records = response.context['low_stock_records']
        weekly_sales_data = json.loads(response.context['weekly_sales_data'])

        # Popular records should be sorted descending by total sold
        self.assertTrue(
            all(popular_records[i]['total_sold'] >=
                popular_records[i+1]['total_sold']
                for i in range(len(popular_records)-1)))
        # Low stock records should be sorted ascending by quantity
        self.assertTrue(
            all(low_stock_records[i].quantity <=
                low_stock_records[i+1].quantity
                for i in range(len(low_stock_records)-1)))
        # Weekly sales data should have labels and totals
        self.assertIn('labels', weekly_sales_data)
        self.assertIn('totals', weekly_sales_data)
        self.assertEqual(len(weekly_sales_data['labels']), len(
            weekly_sales_data['totals']))
