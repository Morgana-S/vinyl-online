from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .forms import CheckoutForm
from .models import Order, OrderItem
from profiles.models import DeliveryAddress
from records.models import Record
# Create your views here.


def checkout_view(request):
    """
    View for checking out an order.
    """
    basket = request.session.get('basket', {})
    if not basket:
        messages.warning(request, 'Your basket is empty.')
        return redirect('view_basket')

    if request.method == 'POST':
        form = CheckoutForm(request.POST, user=request.user)
        if form.is_valid():
            order = form.save(commit=False)

            if request.user.is_authenticated:
                order.user = request.user
                order.full_name = form.cleaned_data.get('full_name') or (
                    request.user.profile.full_name() if hasattr(
                        request.user, 'profile') else ''
                )
                order.phone_number = form.cleaned_data.get('phone_number') or (
                    request.user.profile.contact_phone_number if hasattr(
                        request.user, 'profile') else ''
                )
                order.email = form.cleaned_data.get('email') or (
                    request.user.profile.contact_email if hasattr(
                        request.user, 'profile') else ''
                )

                saved_address = form.cleaned_data.get('saved_address')
                if saved_address:
                    order.address_line1 = saved_address.address_line1
                    order.address_line2 = saved_address.address_line2
                    order.city = saved_address.city
                    order.postcode = saved_address.postcode
                else:
                    order.address_line1 = form.cleaned_data.get(
                        'address_line1')
                    order.address_line2 = form.cleaned_data.get(
                        'address_line2')
                    order.city = form.cleaned_data.get('city')
                    order.postcode = form.cleaned_data.get('postcode')

                if (request.user.is_authenticated and
                        form.cleaned_data.get('save_new_address')):
                    DeliveryAddress.objects.create(
                        user=request.user,
                        label='New Delivery Address',
                        address_line1=order.address_line1,
                        address_line2=order.address_line2,
                        city=order.city,
                        postcode=order.postcode,
                    )

        order.subtotal_cost = 0
        order.delivery_cost = 0
        order.grand_total_cost = 0
        order.save()

        for record_id, quantity in basket.items():
            record = get_object_or_404(Record, pk=record_id)
            OrderItem.objects.create(
                order=order,
                record=record,
                quantity=quantity
            )

        request.session['basket'] = {}
        messages.success(request, 'Your order has been placed successfully.')
        url = (f"{reverse(
            'order_confirmation',
            kwargs={'order_uuid': order.uuid})}?from_checkout=True")
        return redirect(url)
    else:
        form = CheckoutForm(user=request.user)

    context = {
        'form': form
    }
    return render(request, 'checkout/checkout.html', context)


def order_confirmation_view(request, order_uuid):
    """
    View for the order confirmation page, as well as for seeing confirmation
    for past orders.
    """
    order = get_object_or_404(Order, uuid=order_uuid)
    from_checkout = request.GET.get('from_checkout') == 'True'

    context = {
        'order': order,
        'from_checkout': from_checkout
    }

    return render(request, 'checkout/order_confirmation.html', context)
