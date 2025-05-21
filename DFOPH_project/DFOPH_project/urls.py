from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('DFOPH_accounts.urls')),  # This includes login/ route
]
