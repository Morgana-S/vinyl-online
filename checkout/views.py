from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from decimal import Decimal, ROUND_HALF_UP
from .forms import CheckoutForm
from .models import Order, OrderItem
from profiles.models import DeliveryAddress
from records.models import Record
import json
import stripe
# Create your views here.


def checkout_view(request):
    """
    View for checking out an order.
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY
    basket = request.session.get('basket', {})
    if not basket:
        messages.warning(request, 'Your basket is empty.')
        return redirect('index')

    subtotal = sum(
        get_object_or_404(Record, pk=record_id).price * quantity
        for record_id, quantity in basket.items()
    )
    subtotal = Decimal(subtotal)

    delivery_modifier = Decimal(str(settings.STANDARD_DELIVERY_MODIFIER))
    delivery = Decimal('0.00') if subtotal > Decimal(
        settings.FREE_DELIVERY_THRESHOLD) else (
            subtotal * delivery_modifier).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP)

    grand_total = (subtotal + delivery).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP)

    intent_id = request.session.get('payment_intent_id')
    intent = None
    if intent_id:
        try:
            existing_intent = stripe.PaymentIntent.retrieve(intent_id)
            if existing_intent.status in [
                'requires_payment_method',
                'requires_confirmation'
            ]:
                intent = existing_intent
        except stripe.error.InvalidRequestError:
            intent = None

    if not intent:
        intent = stripe.PaymentIntent.create(
            amount=int(grand_total * 100),
            currency='gbp',
            metadata={
                'basket': json.dumps(basket),
                'user': (str(request.user.username) if
                         request.user.is_authenticated else 'guest')
            }
        )
        request.session['payment_intent_id'] = intent.id

    form = CheckoutForm(user=request.user)

    if request.method == 'POST':
        data = json.loads(request.body)
        stripe_pid = data.get('stripe_pid')
        form = CheckoutForm(data, user=request.user)

        if form.is_valid():
            order = form.save(commit=False)
            order.subtotal_cost = subtotal
            order.delivery_cost = delivery
            order.grand_total_cost = grand_total
            order.stripe_pid = stripe_pid

            if request.user.is_authenticated:
                order.user = request.user
                saved_address = form.cleaned_data.get('saved_address')
                save_new = form.cleaned_data.get('save_new_address')
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
                    if save_new:
                        DeliveryAddress.objects.create(
                            user=request.user,
                            label='New Address',
                            address_line1=order.address_line1,
                            address_line2=order.address_line2,
                            city=order.city,
                            postcode=order.postcode
                        )
            else:
                order.address_line1 = form.cleaned_data.get(
                    'address_line1')
                order.address_line2 = form.cleaned_data.get('address_line2')
                order.city = form.cleaned_data.get('city')
                order.postcode = form.cleaned_data.get('postcode')

            order.save()

            for record_id, quantity in basket.items():
                record = get_object_or_404(Record, pk=record_id)
                OrderItem.objects.create(
                    order=order, record=record, quantity=quantity
                )

                if record.quantity is not None:
                    record.quantity = max(record.quantity - quantity, 0)
                    record.save()

            # Confirmation Email
            confirmation_url = request.build_absolute_uri(reverse(
                'order_confirmation', kwargs={'order_uuid': order.uuid}
            ))
            subject = (
                f'Vinyl Online - Your Order Confirmation Ref: {order.uuid}')
            html_message = render_to_string(
                'emails/order_confirmation.html',
                {'order': order,
                 'confirmation_url': confirmation_url}
            )
            plain_message = strip_tags(html_message)
            send_mail(
                subject,
                plain_message,
                None,
                [order.email],
                html_message=html_message
            )

            request.session['basket'] = {}
            request.session.pop('payment_intent_id', None)

            return JsonResponse({
                'success': True,
                'order_uuid': str(order.uuid)
            })
        else:
            return JsonResponse({'errors': form.errors}, status=400)

    context = {
        'form': form,
        'client_secret': intent.client_secret,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'grand_total': grand_total,
        'subtotal_cost': subtotal,
        'delivery_cost': delivery
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


@login_required
def full_order_history_view(request):
    """
    View for rendering all user orders.
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'orders': orders
    }

    return render(request, 'checkout/order_history.html', context)
