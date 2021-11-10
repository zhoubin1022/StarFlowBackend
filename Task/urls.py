from django.urls import path

from Task import admin

urlpatterns = [
    path(r'admin/', admin.site.urls),
]
