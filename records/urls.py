from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('add-artist/', views.add_artist_view, name='add_artist'),
    path('add-record/', views.add_record_view, name='add_record'),
    path('all-records/', views.all_records_view, name='all_records'),
    path('artist/<slug:artist_slug>/',
         views.artist_detail_view,
         name='artist_detail'
         ),
    path('analytics/', views.analytics_page_view, name='analytics'),
    path('async-search/', views.search_records_async, name='async_search'),
    path('delete-artist/<slug:artist_slug>/',
         views.delete_artist_view,
         name='delete_artist'),
    path('delete-record/<slug:record_slug>/',
         views.delete_record_view, name='delete_record'),
    path('edit-artist/<slug:artist_slug>/',
         views.edit_artist_view,
         name='edit_artist'),
    path('edit-record/<slug:record_slug>/',
         views.edit_record_view,
         name='edit_record'),
    path('genre/<slug:genre_name>/',
         views.browse_by_genre_view,
         name='browse_by_genre'),
    path('latest-releases/',
         views.latest_releases_view,
         name='latest_releases'
         ),
    path('search/', views.search_records_view, name='search'),
    path(
        'record/<slug:record_slug>/',
        views.record_detail_view,
        name='record_detail'),
]
