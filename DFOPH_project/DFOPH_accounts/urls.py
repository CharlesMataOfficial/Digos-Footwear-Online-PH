# urls.py
from django.urls import path
from .views import MyTokenObtainPairView, RegisterUserAPIView
from . import views


urlpatterns = [
    # Serve login page at /accounts/login/
    path('', views.login_page, name='login_page'),

    # API endpoint for login (JWT token obtain)
    path('api/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/register/', RegisterUserAPIView.as_view(), name='register'),
]