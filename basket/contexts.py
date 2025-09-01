from django.conf import settings
from decimal import Decimal


def basket_contents(request):
    """
    Context processor for basket items to allow for the basket to be accessed
    throughout the site.
    """
    basket_items = []
    subtotal_cost = 0
    record_count = 0

    if subtotal_cost < Decimal(settings.FREE_DELIVERY_THRESHOLD):
        delivery_cost = (
            subtotal_cost * Decimal(settings.STANDARD_DELIVERY_MODIFIER))
        free_delivery_amount_required = (
            settings.FREE_DELIVERY_THRESHOLD - subtotal_cost)
    else:
        delivery_cost = 0
        free_delivery_amount_required = 0

    grand_total = subtotal_cost + delivery_cost

    context = {
        'basket_items': basket_items,
        'record_count': record_count,
        'subtotal_cost': subtotal_cost,
        'delivery_cost': delivery_cost,
        'free_delivery_amount_required': free_delivery_amount_required,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total
    }
    return context
