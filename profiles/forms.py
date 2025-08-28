from django import forms
from .models import UserProfile
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import RegionalPhoneNumberWidget

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'first_name', 'last_name', 'contact_email', 'contact_phone_number'
            ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field.help_text:
                field.widget.attrs['placeholder'] = field.help_text
        self.fields['contact_phone_number'].widget = RegionalPhoneNumberWidget()