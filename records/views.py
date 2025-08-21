from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Record, Artist, RecordImage, Genre

# Create your views here.


def index_view(request):
    """
    View for the index page. Obtains information about the latest releases and
    a specific category of music (currently Pop) and returns the top 5 rated
    albums.

    TODO: Add community ratings to records so that the ratings can be sorted
    and a featured genre section added according to popularity.
    """
    latest_releases = Record.objects.order_by('-created_at')[:5]
    featured_genre = 'Pop'
    featured_genre_records = Record.objects.filter(
        genre__name='Pop').order_by('-release_year')[:5]

    context = {
        'latest_releases': latest_releases,
        'featured_genre': featured_genre,
        'featured_genre_records': featured_genre_records
    }

    return render(request, 'records/index.html', context)


def search_records_view(request):
    """
    View for searching for records. Obtains the query information from the
    input on the search bar. Then displays both artists and records that match
    the search terms.
    """
    
    SORT_OPTIONS_ARTISTS = {
        'name_asc': 'name',
        'name_desc': '-name',
        'debut_asc': 'debut_year',
        'debut_desc': '-debut_year',
    }

    SORT_OPTIONS_RECORDS = {
        'title_asc': 'title',
        'title_desc': '-title',
        'release_year_asc': 'release_year',
        'release_year_desc': '-release_year',
        'price_asc': 'price',
        'price_desc': '-price'
    }

    sort_by_artists = request.GET.get('sort_artist', 'name')
    sort_by_records = request.GET.get('sort_record', 'title')

    order_field_artists = SORT_OPTIONS_ARTISTS.get(sort_by_artists, 'name')
    order_field_records = SORT_OPTIONS_RECORDS.get(sort_by_records, 'title')

    query = request.GET.get('q', '')
    artists = Artist.objects.filter(Q(name__icontains=query)).order_by(
        order_field_artists
    )
    records = Record.objects.filter(Q(title__icontains=query)).order_by(
        order_field_records
    )

    paginator_artists = Paginator(artists, 8)
    artists_page_number = request.GET.get('artists_page')
    artists_page_obj = paginator_artists.get_page(artists_page_number)

    paginator_records = Paginator(records, 8)
    records_page_number = request.GET.get('records_page')
    records_page_obj = paginator_records.get_page(records_page_number)

    context = {
        'query': query,
        'artists': artists,
        'records': records,
        'artists_results': artists_page_obj,
        'records_results': records_page_obj,
    }

    return render(request, 'records/search.html', context)
