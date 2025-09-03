from django import forms
from django.forms import inlineformset_factory
from django_summernote.widgets import SummernoteWidget
from .models import Record, RecordImage, Artist


class RecordForm(forms.ModelForm):
    """
    Form for editing/adding record details.
    """
    class Meta:
        model = Record
        fields = [
            'title', 'slug', 'artist', 'release_year', 'genre', 'size', 'rpm',
            'description', 'price', 'quantity', 'hidden'
        ]
        labels = {
            'title': 'Title*',
            'slug': 'Slug',
            'artist': 'Artist*',
            'release_year': 'Release Year',
            'genre': 'Genres',
            'size': 'Record Size*',
            'rpm': 'Record RPM*',
            'description': 'Record Details',
            'price': 'Price*',
            'quantity': 'Stock Available*',
            'hidden': 'Hide Record from Sale?'
        }
        widgets = {
            'description': SummernoteWidget()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ != 'CheckboxInput':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-check-input'


RecordImageFormSet = inlineformset_factory(
    Record,
    RecordImage,
    fields=('image', 'image_type'),
    extra=5,
    can_delete=True
)


class ArtistForm(forms.ModelForm):
    """
    Form for adding/editing artist
    """
    class Meta:
        model = Artist
        fields = '__all__'
        labels = {
            'name': 'Name*',
            'slug': 'Slug',
            'image': 'Artist Profile Image*',
            'debut_year': 'Debut Year',
            'bio': 'Short Bio',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
