from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_profile_view, name='profile'),
    path('add-delivery-address/',
         views.create_delivery_address_view,
         name='add_delivery_address'),
    path('create-edit-profile/',
         views.create_edit_profile_view,
         name='create_edit_profile'),
    path('delete-delivery-address/<uuid:pk>/',
         views.delete_delivery_address_view,
         name='delete_delivery_address'),
    path('edit-delivery-address/<uuid:pk>/',
         views.edit_delivery_address_view,
         name='edit_delivery_address'),
]
