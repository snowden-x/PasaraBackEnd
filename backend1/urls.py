from django.urls import path
from . import views

urlpatterns = [
    path('send_food_items/', views.lobby),
]