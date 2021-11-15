from django.urls import path
from Repository import admin
from Repository import views
urlpatterns = [
    path('database_query', views.database_query),
    path('database_query_task_list', views.database_query_task_list),
    path('database_project_insert_one', views.database_project_insert_one),
    path('identity_change', views.identity_change)
]
