from django.test import TestCase
from django.urls import reverse
from .models import Artist, Record


class SearchRecordsViewTests(TestCase):
    """
    TestCase for the search_records_view.
    """
    def setUp(self):
        for i in range(20):
            Artist.objects.create(name=f'Artist {i}')

    def test_view_status_code_and_tempate(self):
        """
        Tests whether the request is successful and whether the right template
        is used.
        """
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'records/search.html')
    
    def test_view_returns_artist_results(self):
        """
        Tests whether a blank query returns results for artists. 
        As there are more than 15 artists at time of writing, the result
        should equal at least 15.
        """
        response = self.client.get(reverse('search'))
        artists_results = response.context['artists_results']
        self.assertGreaterEqual(artists_results.paginator.count, 15)