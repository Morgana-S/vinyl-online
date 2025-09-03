from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('search/', views.search_records_view, name='search'),
    path('async-search/', views.search_records_async, name='async_search'),
    path(
        'record/<slug:record_slug>/',
        views.record_detail_view,
        name='record_detail'),
    path('edit-record/<slug:record_slug>/',
         views.edit_record_view,
         name='edit_record'),
    path('add-record/', views.add_record_view, name='add_record'),
    path('delete-record/<slug:record_slug>/', views.delete_record_view, name='delete_record'),
    path('artist/<slug:artist_slug>/',
         views.artist_detail_view,
         name='artist_detail'
         ),
    path('genre/<slug:genre_name>/',
         views.browse_by_genre_view,
         name='browse_by_genre'),
    path('all-records/', views.all_records_view, name='all_records'),
    path('latest-releases/',
         views.latest_releases_view,
         name='latest_releases'
         ),
]
