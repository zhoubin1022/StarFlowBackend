from django.urls import path
from User import admin, views

urlpatterns = [
    path('wxlogin', views.wxLogin),
    path('githublogin', views.githubLogin),
    path('repo_search', views.repo_search),
    path('repo_request', views.repo_request),
    path('reply_request', views.reply_request),
    path('request_info', views.request_info),
    path('test', views.test),
    path('showRepo', views.showRepo),
]
