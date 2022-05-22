from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from .permissions import IsLoggedInUserOrAdmin
from .models import User, UserProfile
from datetime import datetime, timedelta
from django.utils.translation import gettext_lazy as _

from rest_framework.decorators import action
# Create your views here.
from .serializers import UserSerializer
import requests

from users_auth_api import serializers


# existing Code
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib import auth
from users_auth_api.sendMsg import sendmsg
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import ManualSchema
from api.serializers import TokenSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Permissions
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]



class SignUpView(View):
    def get(self, request):
        
        return render(request, 'auth_app/sign-up.html')

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(email=email).exists():
            if password == confirm_password:
                user = User.objects.create_user(email=email, first_name=first_name, mobile=str(mobile), last_name=last_name)
                user.set_password(password)
                user.is_active=True
                user.save()
                request.session['id'] = user.id

                return redirect('otp-verify')
                
            else:
                pass

            
        
        return render(request, 'auth_app/sign-up.html', context)



class LoginView(View):
    def get(self, request):
        return render(request, 'auth_app/login.html')
    
    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']

        if email and password: 

            user = auth.authenticate(email=email, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, "You have successfully logged in.")
                    return redirect('customer-home')
                messages.error(request, "You are not active user.")
                return render(request, 'auth_app/login.html')
            messages.error(request, "Invalid user.")
            return render(request, 'auth_app/login.html')
        messages.error(request, "Enter correct email and password.")
        return render(request, 'auth_app/login.html')
    
                    
class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect('login')



def otp_verify(request):
    otpWritten = request.POST.get('otp')

    if not request.user.is_authenticated:
        user_id = request.session.get('id')
    else:
        user_id = request.user.id
    user = User.objects.get(id=user_id)
    
    if not request.POST:
        print(f'{user.get_full_name()} - {user.otp}')
        body = f'Hello {user.get_full_name()} your otp is {user.otp}'
        # sendmsg(user.mobile, body)
        print(sendmsg(user.mobile, body))
        # send sms 
    if request.method == "POST":
        if int(otpWritten) == int(user.otp):
            user.is_PhoneVerified = True
            user.save()
            messages.success(request, "Phone number Verified.")
            return redirect('customer-home')
        messages.error(request, "not valid.")
        return redirect('otp-verify')

    return render(request, 'auth_app/otp_check.html')


class CustomAuthToken(ObtainAuthToken):
    serializer_class = TokenSerializer
    if coreapi is not None and coreschema is not None:
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="email",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Email",
                        description="Valid email for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

obtain_auth_token = CustomAuthToken.as_view()
