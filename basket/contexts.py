from django.conf import settings
from records.models import Record
from decimal import Decimal


def basket_contents(request):
    """
    Context processor for basket items to allow for the basket to be accessed
    throughout the site.
    """
    basket = request.session.get('basket')
    basket_items = []
    subtotal_cost = Decimal('0.00')
    record_count = 0

    for record_id, quantity in basket.items():
        try:
            record = Record.objects.get(id=record_id)
            total_price = record.price * quantity
            subtotal_cost += total_price
            record_count += quantity
            basket_items.append({
                'record_id': record_id,
                'quantity': quantity,
                'record': record,
                'total_price': total_price
            })
        except Record.DoesNotExist:
            continue

    if subtotal_cost < Decimal(settings.FREE_DELIVERY_THRESHOLD):
        delivery_cost = (
            subtotal_cost * Decimal(settings.STANDARD_DELIVERY_MODIFIER))
        free_delivery_amount_required = Decimal(
            settings.FREE_DELIVERY_THRESHOLD - subtotal_cost)
    else:
        delivery_cost = Decimal('0.00')
        free_delivery_amount_required = Decimal('0.00')

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


def basket_contents(request):
    """
    Context processor for basket items to allow for the basket to be accessed
    throughout the site.
    """
    basket = request.session.get('basket', {})
    basket_items = []
    subtotal_cost = Decimal('0.00')
    record_count = 0

    for record_id, quantity in basket.items():
        try:
            record = Record.objects.get(id=record_id)
            total_price = record.price * quantity
            subtotal_cost += total_price
            record_count += quantity
            basket_items.append({
                'record_id': record_id,
                'quantity': quantity,
                'record': record,
                'total_price': total_price
            })
        except Record.DoesNotExist:
            continue

    if subtotal_cost < Decimal(settings.FREE_DELIVERY_THRESHOLD):
        delivery_cost = subtotal_cost * \
            Decimal(settings.STANDARD_DELIVERY_MODIFIER)
        free_delivery_amount_required = Decimal(
            settings.FREE_DELIVERY_THRESHOLD) - subtotal_cost
    else:
        delivery_cost = Decimal('0.00')
        free_delivery_amount_required = Decimal('0.00')

    grand_total = subtotal_cost + delivery_cost

    return {
        'basket_items': basket_items,
        'record_count': record_count,
        'subtotal_cost': subtotal_cost,
        'delivery_cost': delivery_cost,
        'free_delivery_amount_required': free_delivery_amount_required,
        'free_delivery_threshold': Decimal(settings.FREE_DELIVERY_THRESHOLD),
        'grand_total': grand_total
    }
