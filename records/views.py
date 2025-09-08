from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Sum, F
from django.db.models.functions import TruncWeek
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from checkout.models import Order, OrderItem
from .forms import RecordForm, RecordImageFormSet, ArtistForm
from .models import Record, Artist, Genre, Review
import json
# Create your views here.


def index_view(request):
    """
    View for the index page. Obtains information about the latest releases and
    a specific category of music (currently Pop) and returns the top 5 rated
    albums.

    **Context**
    ``latest_releases``
        The 5 most recently added records to the site.

    ``featured_genre``
        String representing the currently featured genre.

    ``featured_genre_records``
        Record objects, filtered by the featured_genre string in their genre
        category. These records then have their review rating annotated
        so they can then be sorted by this.

    **Template**
    :template:`records/index.html`
    """
    latest_releases = Record.objects.filter(
        hidden=False).order_by('-created_at')[:5]
    featured_genre = 'Pop'
    featured_genre_records = Record.objects.filter(
        genre__name=featured_genre, hidden=False).annotate(
            avg_rating=Avg('record_reviews__record_rating')).order_by(
                'avg_rating')[:5]

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

    **Context**
    ``query``
        The user's search query.

    ``artists``
        Artist objects with a name that contains the user's search query.

    ``records``
        Record objects with a name that contains the user's search query.

    ``artist_results``
        Paginated list of results for the artists.

    ``records_results``
        Paginated list of results for the records.

    **Template**
    :template:`records/search.html`
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
    records = Record.objects.filter(Q(
        title__icontains=query, hidden=False)).order_by(
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


def search_records_async(request):
    """
    Async view for the search artists/records search bar.
    Returns a JSON response of results that match the user's typed query,
    and appends it to the search results div.
    """
    query = request.GET.get('q', '')
    results = []

    if query:
        records = Record.objects.filter(
            title__icontains=query, hidden=False)[:5]
        artists = Artist.objects.filter(name__icontains=query)[:2]

        for result in records:
            results.append({
                'type': 'record',
                'slug': result.slug,
                'name': result.title,
                'artist': result.artist.name,
            })

        for result in artists:
            results.append({
                'type': 'artist',
                'slug': result.slug,
                'name': result.name,
            })

        return JsonResponse(results, safe=False)


def record_detail_view(request, record_slug):
    """
    View for individual record pages. Obtains information from the record
    instance in the database and populates it.

    **Context**
    ``record``
        The record the view pertains to.

    ``approved_reviews``
        Reviews that have been approved for this record.

    ``reviews``
        All reviews that exist for this record, approved or not.

    ``reviews_page``
        Paginated list of reviews.

    ``is_reviewable``
        Confirms whether the user is eligible to leave a review.

    ``has_reviewed``
        Confirms whether the user has left a review for this record.

    **Template**
    :template:`records/record_detail.html`
    """
    record = get_object_or_404(Record, slug=record_slug)
    reviews = Review.objects.all().filter(record=record)
    approved_reviews = Review.objects.filter(
        record=record, is_approved=True).exists()

    if request.user.is_authenticated:
        is_reviewable = Order.objects.filter(
            user=request.user, items__record=record,
            status='delivered').exists()
        has_reviewed = Review.objects.filter(
            author=request.user, record=record).exists()
    else:
        is_reviewable = False
        has_reviewed = False

    for review in reviews:
        review.is_deletable = (request.user.is_authenticated
                               and review.author == request.user)

    paginator = Paginator(reviews, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'record': record,
        'approved_reviews': approved_reviews,
        'reviews': reviews,
        'reviews_page': page_obj,
        'is_reviewable': is_reviewable,
        'has_reviewed': has_reviewed
    }

    return render(request, 'records/record_detail.html', context)


@login_required
def add_record_view(request):
    """
    View for adding new records. Uses the Record form to populate record
    information and create a new record object.

    **Context**
    ``form``
        The form used to add record details.

    ``formset``
        Formset used for RecordImages.

    **Template**
    :template:`records/create_record.html`
    """
    if request.user.is_staff:
        if request.method == 'POST':
            form = RecordForm(request.POST)
            formset = RecordImageFormSet(request.POST, request.FILES)
            if form.is_valid() and formset.is_valid():
                record = form.save(commit=False)
                record.save()
                formset.instance = record
                formset.save()
                messages.success(request, 'New record has been created and '
                                 'images attached.')
                return redirect('index')

        else:
            form = RecordForm()
            formset = RecordImageFormSet()
    else:
        messages.error(request, 'You must be a member of staff to access this '
                       'part of the website.')
        return redirect('index')

    context = {
        'form': form,
        'formset': formset,
    }

    return render(request, 'records/create_record.html', context)


@login_required
def edit_record_view(request, record_slug):
    """
    View for editing record pages. Serves the EditRecordForm to the user
    and enables them to change record details.

    **Context**
    ``form``
        The form used to add record details.

    ``formset``
        Formset used for RecordImages.

    **Template**
    :template:`records/edit_record.html`
    """
    queryset = Record.objects.all()
    record = get_object_or_404(queryset, slug=record_slug)

    if request.user.is_staff:
        if request.method == 'POST':
            form = RecordForm(request.POST, instance=record)
            formset = RecordImageFormSet(
                request.POST, request.FILES, instance=record)
            if form.is_valid() and formset.is_valid():
                form.save()
                formset.save()
                messages.success(request,
                                 'Record details successfully edited.')
                return redirect('record_detail', record_slug=record_slug)
        else:
            form = RecordForm(instance=record)
            formset = RecordImageFormSet(instance=record)
    else:
        messages.error(request, 'You must be a member of staff to access this '
                       'part of the website.')
        return redirect('record_detail', record_slug=record_slug)

    context = {
        'form': form,
        'formset': formset
    }

    return render(request, 'records/edit_record.html', context)


@login_required
def delete_record_view(request, record_slug):
    """
    View for deleting records. Listens for a POST request under specific
    conditions (permissions are determined by whether the user is staff)
    and deletes the record if correct.
    """
    record = get_object_or_404(Record, slug=record_slug)
    if request.user.is_staff:
        if request.method == 'POST':
            record.delete()
            messages.success(request, 'This record has now been deleted.')
            return redirect('index')
        else:
            return redirect('record_detail', record_slug=record_slug)
    else:
        messages.error(request, 'You must be a member of staff to delete '
                       'records.')
        return redirect('record_detail', record_slug=record_slug)


def artist_detail_view(request, artist_slug):
    """
    View for individual artist pages. Obtains information from the artist
    instance in the database and populates the page with it.
    """
    queryset = Artist.objects.all()
    artist = get_object_or_404(queryset, slug=artist_slug)
    records = Record.objects.all().filter(artist=artist, hidden=False)
    paginator = Paginator(records, 6)
    page_number = request.GET.get('page')
    record_results = paginator.get_page(page_number)

    context = {
        'artist': artist,
        'record_results': record_results
    }

    return render(request, 'records/artist_detail.html', context)


@login_required
def add_artist_view(request):
    """
    View for adding new artists. Uses the Artist form to populate artist
    information and create a new artist object.

    **Context**
    ``form``
        The form used to add artist details.

    **Template**
    :template:`records/create_artist.html`
    """
    if request.user.is_staff:
        if request.method == 'POST':
            form = ArtistForm(request.POST, request.FILES)
            if form.is_valid():
                artist = form.save()
                artist.save()
                messages.success(request, 'New artist has successfully been '
                                 'created.')
                return redirect('index')
        else:
            form = ArtistForm()
    else:
        messages.error(request, 'You must be a member of staff to access this '
                       'part of the website.')
        return redirect('index')

    context = {
        'form': form
    }

    return render(request, 'records/create_artist.html', context)


@login_required
def edit_artist_view(request, artist_slug):
    """
    View for editing artists. Uses the same form as the add_artist view.

    **Context**
    ``form``
        The form used to edit artist details.

    **Template**
    :template:`records/edit_artist.html`
    """
    artist = get_object_or_404(Artist, slug=artist_slug)
    if request.user.is_staff:
        if request.method == 'POST':
            form = ArtistForm(request.POST, request.FILES, instance=artist)
            if form.is_valid():
                form.save()
                messages.success(request, 'Artist details have been '
                                 'successfully edited.')
                return redirect('artist_detail', artist_slug=artist_slug)
        else:
            form = ArtistForm(instance=artist)
    else:
        messages.error(request, 'You must be a member of staff to access this '
                       'part of the site.')
        return redirect('index')

    context = {
        'form': form
    }

    return render(request, 'records/edit_artist.html', context)


@login_required
def delete_artist_view(request, artist_slug):
    """
    View for deleting artists. Listens for a POST request from a staff
    user who submits the form for deleting the artist and then subsequently
    deletes that artist.
    """
    artist = get_object_or_404(Artist, slug=artist_slug)
    if request.user.is_staff:
        if request.method == 'POST':
            artist.delete()
            messages.success(request, 'Artist has now been deleted.')
            return redirect('index')
        else:
            return redirect('artist_detail', artist_slug=artist_slug)
    else:
        messages.error(request, 'You must be a member of staff to access this '
                       'part of the site.')
        return redirect('index')


def browse_by_genre_view(request, genre_name):
    """
    View for browsing records by genre. Gets the genre name and obtains
    paginated results for all records with that genre.

    **Context**
    ``genre``
        The genre that user wishes to browse, from the Genre Model.

    ``records``
        Record objects that belong to the chosen genre.
    
    ``record_results``
        Paginated list of record object results.

    **Template**
    :template:`records/browse_by_genre.html`
    """
    SORT_OPTIONS = {
        'title_asc': 'title',
        'title_desc': '-title',
        'release_year_asc': 'release_year',
        'release_year_desc': '-release_year',
        'price_asc': 'price',
        'price_desc': '-price'
    }

    sort_by_records = request.GET.get('sort_record', 'title')
    order_field_records = SORT_OPTIONS.get(sort_by_records, 'title')
    genre = get_object_or_404(Genre, slug=genre_name)
    records = Record.objects.filter(genre=genre, hidden=False).order_by(
        order_field_records
    )
    paginator = Paginator(records, 16)
    page_number = request.GET.get('records_page')
    records_results = paginator.get_page(page_number)

    context = {
        'genre': genre,
        'records': records,
        'records_results': records_results,
    }

    return render(request, 'records/browse_by_genre.html', context)


def all_records_view(request):
    """
    View for browsing all records, with sorting.
    
    **Context**
    ``records``
        Record objects that are available for view.

    ``record_results``
        Paginated record objects.

    **Template**
    :template:`records/all_records.html`
    """
    SORT_OPTIONS_RECORDS = {
        'title_asc': 'title',
        'title_desc': '-title',
        'release_year_asc': 'release_year',
        'release_year_desc': '-release_year',
        'price_asc': 'price',
        'price_desc': '-price'
    }

    sort_by_records = request.GET.get('sort_record', 'title')
    order_field_records = SORT_OPTIONS_RECORDS.get(sort_by_records, 'title')

    records = Record.objects.all().filter(
        hidden=False).order_by(order_field_records)
    paginator = Paginator(records, 16)
    page_number = request.GET.get('records_page')
    records_results = paginator.get_page(page_number)

    context = {
        'records': records,
        'records_results': records_results
    }

    return render(request, 'records/all_records.html', context)


def latest_releases_view(request):
    """
    View for browsing the 16 latest releases.

    **Context**
    ``records``
        The last 16 record objects that were added to the site.

    **Template**
    :template:`records/latest_records.html`
    """
    records = Record.objects.all().filter(
        hidden=False).order_by('-created_at')[:16]

    context = {
        'records': records,
    }

    return render(request, 'records/latest_records.html', context)


@staff_member_required
def analytics_page_view(request):
    """
    View for viewing site analytics such as record purchases, sales, and low
    stock.

    **Context**
    ``popular_records``
        The top 10 most sold record objects.

    ``weekly_sales_data``
        Data formatted for the graph canvas which is obtained from
        weekly_sales, which are the amount of records sold each week.

    ``low_stock_records``
        The 10 records which have the lowest quantity of stock available.

    **Template**
    :template:`records/analytics.html`
    """
    popular_records = (OrderItem.objects.values(
        'record__slug', 'record__title').annotate(
            total_sold=Sum('quantity')).order_by('-total_sold'))[:10]

    weekly_sales = (
        OrderItem.objects.annotate(week=TruncWeek('order__created_at')).values(
            'week'
        ).annotate(total_sales=Sum(F('quantity') * F('record__price')))
        .order_by('week')
    )

    weekly_sales_data = {
        'labels': [sale['week'].strftime('%Y-%m-%d') for sale in weekly_sales],
        'totals': [float(sale['total_sales']) for sale in weekly_sales]
    }

    low_stock_records = Record.objects.all().order_by('quantity')[:10]

    context = {
        'popular_records': popular_records,
        'weekly_sales_data': json.dumps(weekly_sales_data),
        'low_stock_records': low_stock_records
    }

    return render(request, 'records/analytics.html', context)
