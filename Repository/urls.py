from django.urls import path
from Repository import admin
from Repository import views
urlpatterns = [
    path('showRepo', views.showRepo),
    path('showTask', views.showTask),
    path('addRepo', views.addRepo),
    path('getReposByKeyword', views.getReposByKeyword),
    path('getAllMember', views.getAllMember),
    path('changeIdentity', views.changeIdentity),
    path('test', views.test),
    path('getRepos', views.getRepos),
    path('exitRepo', views.exitRepo),
]
