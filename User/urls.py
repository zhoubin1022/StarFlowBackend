from django.urls import path
from User import admin

urlpatterns = [
    path(r'admin/', admin.site.urls),
]
