from django.urls import path
from Repository import admin
from Repository import views
urlpatterns = [
    path('identity_change', views.identity_change),
    path('showRepo', views.showRepo),
    path('showTask', views.showTask),
    path('addRepo', views.addRepo),
    path('getRepos', views.getRepos),
]
