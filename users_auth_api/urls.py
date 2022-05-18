from .views import UserViewSet
from django.urls import include, path
from rest_framework import routers
from .views import SignUpView, LoginView, LogoutView, otp_verify

router = routers.DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('signup',SignUpView.as_view(),name='sign-up'),
    path('login',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('otp-verify/',otp_verify,name='otp-verify'),
]