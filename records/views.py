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

    query = request.GET.get('q', '')
    artists = Artist.objects.filter(Q(name__icontains=query)).order_by(
        'name'
    )
    records = Record.objects.filter(Q(title__icontains=query)).order_by(
        'title'
    )

    paginator = Paginator(records, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'query': query,
        'artists': artists,
        'results': page_obj,
    }

    return render(request,'records/search.html', context)