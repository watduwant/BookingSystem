from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from customer.views import appointment
from store.models import Phlebotomist, Shop, Doctor,Service,ServiceDetailsDay,ServiceDetailsDayTime, OrderService, Pathological_Test_Service
from customer.models import Appointment
from users_auth_api.models import User
from .serializers import UserSerializer, ShopSerializer, DoctorSerializer, ServicedetailDaySerializer, ServicedetailDayTimeSerializer, ServiceSerializer, AppointmentSerializer, HomeSreenSerializer, PutAppointmentSerializer, ClinicDoctorSerializer, PhlebotomistSerializer, OrderServiceSerializer, PathoOrdersSerializer, PathologicalTestServiceSerializer
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
    http_method_names = ['get', 'put', 'patch', 'post']
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        appointment = []
        try:
            appointment = Appointment.objects.filter(Service__ServiceDetailsDayID__ServiceID__Clinic=user.shop) .order_by('Service__ServiceDetailsDayID__ServiceID__Doctor')
        except:
            appointment = []
        return appointment

    def get_serializer_class(self):
        if self.request.method == "GET" or self.request.method == 'POST':
            return AppointmentSerializer
        return PutAppointmentSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        # print(data)
        prevDoc = 'None'
        newdata = []
        docApp = []
        for item in data:
            if prevDoc == 'None':
                docApp.append(item)
                prevDoc = item['doctor']['Name']
            elif item['doctor']['Name'] == prevDoc:
                docApp.append(item)
            elif item['doctor']['Name'] != prevDoc:
                newdata.append(docApp)
                docApp = []
                docApp.append(item)
                prevDoc = item['doctor']['Name']
        newdata.append(docApp)
        return Response(newdata)

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        user = []
        try:
            user = User.objects.filter(status='so')
        except:
            user = []
        return user

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
        clinic = []
        user_shop = None
        try:
            user_shop = self.request.user.shop
        except:
            user_shop = None
        if user_shop != None:
            
            try:
                clinic = Shop.objects.get(Shop_owner=self.request.user)
            except:
                clinic = []
        else: 
            return Service.objects.none()

        service = []
        

        try:
            service = Service.objects.filter(Clinic=clinic)
        except:
            service = []

        return service

class phlebotomistViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PhlebotomistSerializer

    
    def get_queryset(self):
        queryset = []
        try:
            queryset = Phlebotomist.objects.filter(Shop=self.request.user.shop)
        except:
            queryset = []
        return queryset


class OrderServiceViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = OrderServiceSerializer

    def get_queryset(self):
        queryset = []
        try:
            queryset = OrderService.objects.filter(Order__complete=True, PathologicalTestService__Shop=self.request.user.shop)
        except:
            queryset = []
        return queryset

    
    
class PathoOrdersViewSet(viewsets.ReadOnlyModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = PathoOrdersSerializer

    def get_queryset(self):
        queryset = []
        try:
            queryset = OrderService.objects.filter(Order__paymentDone=True, PathologicalTestService__Shop=self.request.user.shop)
        except:
            queryset = []
        return queryset


class PathologicalTestServiceViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PathologicalTestServiceSerializer

    def get_queryset(self):
        queryset = []
        try:
            queryset = Pathological_Test_Service.objects.filter(Shop=self.request.user.shop)
        except:
            queryset = []
        return queryset
    
        
    

    