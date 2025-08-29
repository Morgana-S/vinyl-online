from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import UserProfile, DeliveryAddress
# Register your models here.


@admin.register(UserProfile)
class UserProfileAdmin(SummernoteModelAdmin):
    list_display = ('user', 'full_name', 'contact_email')
    search_fields = ['user__username', 'full_name', 'contact_email']


@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(SummernoteModelAdmin):
    list_display = ('user', 'label', 'city', 'postcode')
    search_fields = ['user__username', 'city', 'postcode']