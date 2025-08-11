from django.contrib import admin
from .models import Artist
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.


@admin.register(Artist)
class ArtistAdmin(SummernoteModelAdmin):
    list_display = ('id', 'name', 'debut_year',)
    search_fields = ['name']
    summernote_fields = ('bio')
    list_filter = ('name', 'debut_year',)
