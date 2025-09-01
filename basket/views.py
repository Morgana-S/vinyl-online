from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from records.models import Record
from django.views.decorators.http import require_POST
# Create your views here.


def view_basket(request):
    """
    View for viewing the total items in the shopping basket.
    """
    return render(request, 'basket/view_basket.html')


@require_POST
def add_to_basket_async(request):
    """
    View for adding items to the basket. Utilises AJAX for a smoother user
    experience.
    """
    record_id = request.POST.get('record_id')
    quantity = int(request.POST.get('quantity', 1))
    record = get_object_or_404(Record, id=record_id)

    if 'basket' not in request.session:
        request.session['basket'] = {}

    basket = request.session.get('basket', {})

    new_quantity = basket.get(str(record_id), 0) + quantity

    basket[str(record_id)] = min(new_quantity, 9)

    request.session['basket'] = basket
    request.session.modified = True

    basket_count = sum(basket.values())

    if new_quantity > 9:
        toast_header = 'Maximum Quantity Reached'
        toast_message = ('Unable to add record to basket -'
                         ' purchases capped at 9 per order.')
    else:
        toast_header = 'Added to Basket'
        toast_message = f'Added {quantity} x {record.title} to your basket!'

    return JsonResponse({
        'toast_header': toast_header,
        'toast_message': toast_message,
        'basket_count': basket_count
    })
