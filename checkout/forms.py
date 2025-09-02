from .models import Order
from profiles.models import DeliveryAddress
from django import forms


class CheckoutForm(forms.ModelForm):
    saved_address = forms.ModelChoiceField(
        queryset=DeliveryAddress.objects.none(),
        required=False,
        empty_label='--- Select a saved address ---',
        widget=forms.Select(attrs={'class': 'form-select mb-3'})
    )
    save_new_address = forms.BooleanField(
        required=False,
        initial=False,
        label='Save this address for future use',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Order
        fields = [
            'full_name',
            'phone_number',
            'email',
            'address_line1',
            'address_line2',
            'city',
            'postcode',
        ]
        labels = {
            'full_name': 'Full Name*',
            'phone_number': 'Phone Number*',
            'email': 'Email Address*',
            'address_line1': 'Address Line 1*',
            'address_line2': 'Address Line 2',
            'city': 'City',
            'postcode': 'Postcode*'
        }
        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": "form-control mb-1"}),
            "address_line1": forms.TextInput(
                attrs={"class": "form-control mb-1"}),
            "address_line2": forms.TextInput(
                attrs={"class": "form-control mb-1"}),
            "city": forms.TextInput(attrs={"class": "form-control mb-1"}),
            "postcode": forms.TextInput(attrs={"class": "form-control mb-1"}),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control mb-1"}),
            "email": forms.EmailInput(attrs={"class": "form-control mb-1"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated:
            self.fields['saved_address'].queryset = (
                DeliveryAddress.objects.filter(user=user))

            if hasattr(user, 'profile'):
                profile = user.profile

                if not self.fields['phone_number'].initial:
                    self.fields['phone_number'].initial = (
                        profile.contact_phone_number)

                if not self.fields['email'].initial:
                    self.fields['email'].initial = (
                        profile.contact_email
                    )

                if not self.fields['full_name'].initial:
                    self.fields['full_name'].initial = profile.full_name()
        else:
            self.fields.pop('saved_address')
