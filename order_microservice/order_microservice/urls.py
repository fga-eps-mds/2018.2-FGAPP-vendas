from django.contrib import admin
from django.urls import path, include
from .version_helper import status

urlpatterns = [
    path('', status),
    path('admin/', admin.site.urls),
    path('api/', include('orders.urls')),
]
