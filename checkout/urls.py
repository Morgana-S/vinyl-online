from django.urls import path
from . import views, webhook

urlpatterns = [
    path('', views.checkout_view, name='checkout'),
    path('order/<uuid:order_uuid>/',
         views.order_confirmation_view,
         name='order_confirmation'),
    path('stripe/webhook/', webhook.stripe_webhook, name='stripe_webhook')
]
