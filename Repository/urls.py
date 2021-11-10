from django.urls import path
from Repository import admin

urlpatterns = [
    path(r'admin/', admin.site.urls),
]
