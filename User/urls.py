from django.urls import path
from User import admin, views

urlpatterns = [
    path('wxlogin', views.wxLogin),
    path('test', views.test)
]
