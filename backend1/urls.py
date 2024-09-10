from django.urls import path
from . import views

urlpatterns = [
    path('editables/', views.editables),
]
