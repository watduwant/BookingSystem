from .views import SignUpView, LoginView, LogoutView
from django.urls import path,include
urlpatterns = [
        path('',SignUpView.as_view(),name='sign-up'),
        path('login',LoginView.as_view(),name='login'),
        path('logout',LogoutView.as_view(),name='logout'),
        ]
