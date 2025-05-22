from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.buyers_dashboard, name='buyers_dashboard'),
]