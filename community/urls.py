from django.urls import path
from . import views

urlpatterns = [
    path('support/contact/',
         views.create_support_ticket_view, name='create_support_ticket'),
    path('support/ticket/<uuid:pk>',
         views.ticket_detail_view, name='ticket_detail'),
    path('support/tickets/',
         views.support_ticket_history_view,
         name='support_ticket_history'),
    path('who-we-are/', views.about_page_view, name='about'),
    path('newsletter/', views.newsletter_subscribe_view, name='newsletter'),
    path('add-review/<slug:record_slug>/',
         views.add_review_view,
         name='add_review'),
    path('delete-review/<int:review_id>/',
         views.delete_review_view,
         name='delete_review'),
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy')
]
