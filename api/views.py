from django.shortcuts import render
from rest_framework import viewsets
from store.models import Shop, Doctor,Service,ServiceDetailsDay,ServiceDetailsDayTime
from customer.models import Appointment
# from django.contrib.auth.models import User
from auth_app.models import User
from .serializers import UserSerializer, ShopSerializer, DoctorSerializer, ServicedetailDaySerializer,ServicedetailDayTimeSerializer, ServiceSerializer, AppointmentSerializer
# Create your views here.

class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServicedetailDayViewSet(viewsets.ModelViewSet):
    queryset = ServiceDetailsDay.objects.all()
    serializer_class = ServicedetailDaySerializer
    
class ServicedetailDayTimeViewSet(viewsets.ModelViewSet):
    queryset = ServiceDetailsDayTime.objects.all()
    serializer_class = ServicedetailDayTimeSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

# class ProfileViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = ProfileSerializer

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(status='so')
    