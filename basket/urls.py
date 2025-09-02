from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_basket, name='view_basket'),
    path('add-to-basket/',
         views.add_to_basket_async_view,
         name='add_to_basket'),
    path('remove-from-basket/<int:record_id>/',
         views.remove_from_basket_view,
         name='remove_basket_item')

]
