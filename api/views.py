from asyncio.windows_events import NULL
from contextlib import nullcontext
from xmlrpc.client import ResponseError
from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from store.models import Shop, Doctor,Service,ServiceDetailsDay,ServiceDetailsDayTime
from customer.models import Appointment
from auth_app.models import User
from .serializers import UserSerializer, ShopSerializer, DoctorSerializer, ServicedetailDaySerializer, ServicedetailDayTimeSerializer, ServiceSerializer, AppointmentSerializer, HomeSreenSerializer, PutAppointmentSerializer, ClinicDoctorSerializer, PutDoctorSerializer
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
    http_method_names = ['get', 'put', 'patch']
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Appointment.objects.filter(Service__ServiceDetailsDayID__ServiceID__Clinic=user.shop) 

    def get_serializer_class(self):
        if self.request.method == "GET":
            return AppointmentSerializer
        return PutAppointmentSerializer

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(status='so')

# class HomeScreenViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
#     queryset = Shop.objects.all()
#     serializer_class = HomeSreenSerializer

from rest_framework.response import Response

class HomeScreenViewset(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            shop = Shop.objects.get(Shop_owner=request.user)
            serializer = HomeSreenSerializer(shop)
            return Response(serializer.data)
        except Shop.DoesNotExist:
            return Response({"error": "You are not the ownwer or any shop"})

class ViewDoctorViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ClinicDoctorSerializer
    
    def get_queryset(self):
        if self.request.user.shop:
            clinic = Shop.objects.get(Shop_owner=self.request.user)
        else: 
            return Service.objects.none()

        return Service.objects.filter(Clinic=clinic)



    def get_serializer_class(self):
        if self.request.method == 'GET':
            if not self.request.user.shop:
                return Response({"error": "You are not the ownwer or any shop"})
            return ClinicDoctorSerializer
        return PutDoctorSerializer
        
    

    