from django.urls import path
from Task import views
from Task import admin

urlpatterns = [
    path('deps', views.getDevelopers)
]
