from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Order, OrderItem
# Register your models here.


class OrderItemAdminInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('item_total',)


@admin.register(Order)
class OrderAdmin(SummernoteModelAdmin):
    list_display = (
        'uuid', 'created_at', 'status', 'user', 'full_name', 'email')
    search_fields = [
        'uuid', 'status', 'user__username', 'full_name', 'email',
        'phone_number']
    # Leaving address fields open so delivery address can be changed
    # as part of support operations
    readonly_fields = ('uuid', 'created_at', 'user', 'full_name', 'stripe_pid')
    list_filter = ('status',)
    ordering = ('-created_at',)
    inlines = (OrderItemAdminInline,)
