from rest_framework_simplejwt.views import TokenObtainPairView
from DFOPH_accounts.serializers import MyTokenObtainPairSerializer, UserRegistrationSerializer
from django.shortcuts import render, redirect
from DFOPH_accounts.models import User, Role
from DFOPH_buyers.models import BuyersProfile
from DFOPH_sellers.models import SellersProfile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny



# 🔵 Create a view that uses your custom serializer
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

def login_page(request):
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address = request.POST['address']
        role_name = request.POST['role']  # 'buyer' or 'seller'

        role = Role.objects.get(name=role_name)

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            firstname=first_name,
            lastname=last_name,
            address=address,
            role=role,
            status='active'
        )

        # Create role-specific profile
        if role_name == 'buyer':
            BuyersProfile.objects.create(user=user, phone='', address=address)
        elif role_name == 'seller':
            SellersProfile.objects.create(user=user, store_name='', store_description='')

        return redirect('login')  # Or redirect to homepage

class RegisterUserAPIView(APIView):
    permission_classes = [AllowAny]  # ✅ Allow unauthenticated users
    # This method will handle POST requests to register a new user
    def post(self, request):
        # Pass the incoming JSON data to the serializer
        serializer = UserRegistrationSerializer(data=request.data)

        # If the data is valid (passes validation in serializer)
        if serializer.is_valid():
            serializer.save()  # Save the user (calls create method)
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)

        # If validation fails, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)