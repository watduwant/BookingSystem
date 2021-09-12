from django.shortcuts import render, redirect
from django.views import View
from . models import Profile
from django.contrib.auth.models import User
from django.contrib import auth


# Create your views here.


class SignUpView(View):
    def get(self, request):
        
        return render(request, 'auth_app/sign-up.html')

    def post(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=email).exists():
            if password == confirm_password:
                user = User.objects.create_user(username=email, email=email,  first_name=first_name, last_name=last_name)
                user.set_password(password)
                user.is_active=True
                user.save()
                return render(request, 'auth_app/login.html', context)
                
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

            user = auth.authenticate(username=email, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    return redirect('customer-home')
                
                return render(request, 'auth_app/login.html')
            
            return render(request, 'auth_app/login.html')
        
        return render(request, 'auth_app/login.html')
    
                    
class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect('login')

