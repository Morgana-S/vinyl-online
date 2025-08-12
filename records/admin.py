from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Artist, Genre, Record
# Register your models here.


@admin.register(Artist)
class ArtistAdmin(SummernoteModelAdmin):
    list_display = ('id', 'name', 'debut_year',)
    search_fields = ['name']
    summernote_fields = ('bio',)
    list_filter = ('name', 'debut_year',)


@admin.register(Genre)
class GenreAdmin(SummernoteModelAdmin):
    list_display = ('id', 'name', 'color',)
    search_fields = ['name']


@admin.register(Record)
class RecordAdmin(SummernoteModelAdmin):
    list_display = ('id', 'artist__name', 'title', 'release_date',)
    search_fields = ['title', 'artist__name']
    list_filter = ('artist__name',)
    summernote_fields = ('description',)