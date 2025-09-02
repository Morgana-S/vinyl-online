from django.shortcuts import render, get_object_or_404, redirect
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
def add_to_basket_async_view(request):
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


def remove_from_basket_view(request, record_id):
    """
    View for removing items from the basket.
    """
    basket = request.session.get('basket', {})
    record_id_str = str(record_id)
    if record_id_str in basket:
        del basket[record_id_str]
        request.session['basket'] = basket
        request.session.modified = True
        basket_count = sum(basket.values())

    return redirect('view_basket')


@require_POST
def update_basket_quantity_view(request):
    """
    View for updating basket quantities and prices.
    """
    basket = request.session.get('basket', {})

    for key, value in request.POST.items():
        if key.startswith('quantity_'):
            record_id = key.split('_')[1]
            try:
                quantity = int(value)
            except ValueError:
                quantity = 1
            
            if quantity <= 0:
                basket.pop(record_id, None)
            else:
                basket[record_id] = min(quantity, 9)
    
    request.session['basket'] = basket
    request.session.modified = True
    
    return redirect('view_basket')