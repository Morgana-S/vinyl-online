from django import forms
from .models import UserProfile, DeliveryAddress
from phonenumber_field.widgets import RegionalPhoneNumberWidget


class UserProfileForm(forms.ModelForm):
    """
    Form for providing user profile information.
    """
    class Meta:
        model = UserProfile
        fields = [
            'first_name', 'last_name', 'contact_email', 'contact_phone_number'
        ]
        labels = {
            'first_name': 'First Name*',
            'last_name': 'Last Name*',
            'contact_email': 'Contact Email',
            'contact_phone_number': 'Contact Phone Number*'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['contact_phone_number'].required = True
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['contact_phone_number'].widget = (
            RegionalPhoneNumberWidget())


class DeliveryAddressForm(forms.ModelForm):
    """
    Form for providing Delivery Address Information.
    """
    class Meta:
        model = DeliveryAddress
        fields = [
            'label', 'address_line1', 'address_line2', 'city', 'postcode'
        ]
        labels = {
            'label': 'Label*',
            'address_line1': 'Address Line 1*',
            'address_line2': 'Address Line 2',
            'city': 'City or Town',
            'postcode': 'Postcode*'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['label'].required = True
        self.fields['address_line1'].required = True
        self.fields['postcode'].required = True
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
