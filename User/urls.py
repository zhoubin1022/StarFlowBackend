from django.urls import path
from User import admin, views

urlpatterns = [
    path('wxlogin', views.wxLogin),
    path('githublogin', views.githubLogin),
    path('repo_search', views.repo_search),
    path('repo_request', views.repo_request)
]
