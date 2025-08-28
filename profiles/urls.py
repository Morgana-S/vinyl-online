from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_profile_view, name='profile'),
    path('create-edit-profile/',
         views.create_edit_profile_view,
         name='create_edit_profile'),

]
