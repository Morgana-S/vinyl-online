from django.shortcuts import render
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
