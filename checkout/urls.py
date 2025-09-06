from django.urls import path
from . import views, webhook

urlpatterns = [
    path('', views.checkout_view, name='checkout'),
    path('order/<uuid:order_uuid>/',
         views.order_confirmation_view,
         name='order_confirmation'),
    path('order-history/', views.full_order_history_view, name='order_history'),
    path('stripe/webhook/', webhook.stripe_webhook, name='stripe_webhook')
]
