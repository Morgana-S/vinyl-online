from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('search/', views.search_records_view, name='search'),
    path(
        'record/<slug:record_slug>',
        views.record_detail_view,
        name='record_detail'
        ),
    path('artist/<slug:artist_slug>',
         views.artist_detail_view,
         name='artist_detail'
         ),
]
