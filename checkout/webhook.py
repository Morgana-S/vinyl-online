from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import stripe


@require_POST
@csrf_exempt
def stripe_webhook(request):
    """

    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid Payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid Signature
        return HttpResponse(status=400)

    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        handle_successful_payment(payment_intent)

    return HttpResponse(status=200)


def handle_successful_payment(payment_intent):
    print('Payment Succeeded:', payment_intent.get('id'))
