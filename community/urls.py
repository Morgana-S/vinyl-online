from django.urls import path
from . import views

urlpatterns = [
    path('support/contact/',
         views.create_support_ticket_view, name='create_support_ticket'),
    path('support/ticket/<uuid:pk>',
         views.ticket_detail_view, name='ticket_detail'),

]
