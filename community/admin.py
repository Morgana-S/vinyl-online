from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import SupportTicket
# Register your models here.


@admin.register(SupportTicket)
class SupportTicketAdmin(SummernoteModelAdmin):
    list_display = ('user', 'email', 'name', 'category', 'status', 'uuid')
    search_fields = ['user__username', 'email', 'name',
                     'category', 'status', 'uuid']
    list_filter = ('category', 'status')
