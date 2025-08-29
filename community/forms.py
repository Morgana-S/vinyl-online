from django import forms
from .models import SupportTicket
from profiles.models import UserProfile


class SupportTicketForm(forms.ModelForm):
    """
    Form for creating a support ticket.
    """
    class Meta:
        model = SupportTicket
        fields = [
            'name', 'email', 'category', 'description'
        ]
        labels = {
            'name': 'Name*',
            'email': 'Preferred Contact Email Address*',
            'category': 'Issue Category*',
            'description': 'Description of Issue*',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
            field.widget.attrs['class'] = 'form-control'
            if user and user.is_authenticated:
                try:
                    profile = user.profile
                except UserProfile.DoesNotExist:
                    profile = None

                if profile:
                    self.fields['name'].initial = profile.full_name()
                    self.fields['email'].initial = profile.contact_email
                else:
                    self.fields['email'].initial = user.email
