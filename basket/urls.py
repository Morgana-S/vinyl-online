from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_basket, name='view_basket'),
    path('add-to-basket/', views.add_to_basket_async, name='add_to_basket')
]
