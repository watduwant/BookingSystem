from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

# from django.contrib.auth.models import User
from auth_app.models import User
from customer.models import Appointment
from store.models import (
    Phlebotomist,
    Shop,
    Doctor,
    Service,
    ServiceDetailsDay,
    ServiceDetailsDayTime,
    OrderService,
    Pathological_Test_Service
)
from .serializers import (
    UserSerializer,
    ShopSerializer,
    DoctorSerializer,
    ServicedetailDaySerializer,
    ServicedetailDayTimeSerializer,
    ServiceSerializer,
    AppointmentSerializer,
    HomeSreenSerializer,
    PutAppointmentSerializer,
    ClinicDoctorSerializer,
    PhlebotomistSerializer,
    OrderServiceSerializer,
    PathoOrdersSerializer,
    PathologicalTestServiceSerializer,
    AppointmentServicesSerializer,
    ShopListSerializer,
    ServiceListSerializer,
    ServiceDetailDayListTimeSerializer,
    AppointmentListSerializer
)


# Create your views here.

class BaseClass(ModelViewSet):

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        data = {
            "count": len(serializer.data),
            "data": serializer.data,
        }
        return Response(data)


class ShopViewSet(BaseClass):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    def get_serializer(self, *args, **kwargs):
        """
        Use a custom serializer that includes nested objects.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        if self.action == 'list':
            # Use a custom serializer for list actions that includes nested objects
            serializer_class = ShopListSerializer
        if self.action == 'retrieve':
            # Use a custom serializer for retrieve actions that includes nested objects
            serializer_class = ShopListSerializer
        return serializer_class(*args, **kwargs)


class DoctorViewSet(BaseClass):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class ServiceViewSet(BaseClass):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_serializer(self, *args, **kwargs):
        """
        Use a custom serializer that includes nested objects.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        if self.action == 'list':
            # Use a custom serializer for list actions that includes nested objects
            serializer_class = ServiceListSerializer
        if self.action == 'retrieve':
            # Use a custom serializer for retrieve actions that includes nested objects
            serializer_class = ServiceListSerializer
        return serializer_class(*args, **kwargs)


class ServicedetailDayViewSet(BaseClass):
    queryset = ServiceDetailsDay.objects.all()
    serializer_class = ServicedetailDaySerializer

    # def get_serializer(self, *args, **kwargs):
    #     """
    #     Use a custom serializer that includes nested objects.
    #     """
    #     serializer_class = self.get_serializer_class()
    #     kwargs['context'] = self.get_serializer_context()
    #     if self.action == 'list':
    #         # Use a custom serializer for list actions that includes nested objects
    #         serializer_class = ServicedetailListDaySerializer
    #     return serializer_class(*args, **kwargs)


class ServicedetailDayTimeViewSet(BaseClass):
    queryset = ServiceDetailsDayTime.objects.all()
    serializer_class = ServicedetailDayTimeSerializer

    def get_serializer(self, *args, **kwargs):
        """
        Use a custom serializer that includes nested objects.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        if self.action == 'list':
            # Use a custom serializer for list actions that includes nested objects
            serializer_class = ServiceDetailDayListTimeSerializer
        if self.action == 'retrieve':
            # Use a custom serializer for retrieve actions that includes nested objects
            serializer_class = ServiceDetailDayListTimeSerializer
        return serializer_class(*args, **kwargs)


class AppointmentServicesViewset(BaseClass):
    http_method_names = ['get']
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentServicesSerializer

    def get_queryset(self):
        user = self.request.user
        service_id = self.request.query_params.get('service_id', None)
        if service_id:
            return ServiceDetailsDay.objects.filter(ServiceID__Clinic=user.shop, ServiceID__id=service_id)

        return ServiceDetailsDay.objects.filter(ServiceID__Clinic=user.shop).order_by('ServiceID')


class AppointmentViewSet(BaseClass):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = AppointmentSerializer

    def perform_create(self, serializer):
        serializer.save(shop_owner=self.request.user)
        return

    def get_queryset(self):
        queryset = Appointment.objects.all()
        if self.action == 'list':
            queryset = Appointment.objects.filter(shop_owner=self.request.user)
        return queryset

    def get_serializer(self, *args, **kwargs):
        """
        Use a custom serializer that includes nested objects.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        if self.action == 'list':
            # Use a custom serializer for list actions that includes nested objects
            serializer_class = AppointmentListSerializer
        if self.action == 'retrieve':
            # Use a custom serializer for retrieve actions that includes nested objects
            serializer_class = AppointmentListSerializer
        if self.action == 'update':
            # Use a custom serializer for update actions that includes nested objects
            serializer_class = PutAppointmentSerializer
        return serializer_class(*args, **kwargs)


class UserViewSet(BaseClass):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def get_queryset(self):
    #     return User.objects.filter(status='so')


# class HomeScreenViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
#     queryset = Shop.objects.all()
#     serializer_class = HomeSreenSerializer


class HomeScreenViewset(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            shop = Shop.objects.get(Shop_owner=request.user)
            serializer = HomeSreenSerializer(shop)
            return Response(serializer.data)
        except Shop.DoesNotExist:
            return Response({"error": "You are not the ownwer or any shop"})


class ViewDoctorViewset(BaseClass):
    permission_classes = [IsAuthenticated]
    serializer_class = ClinicDoctorSerializer

    def get_queryset(self):
        if self.request.user.shop:
            clinic = Shop.objects.get(Shop_owner=self.request.user)
        else:
            return Service.objects.none()

        return Service.objects.filter(Clinic=clinic)


class phlebotomistViewset(BaseClass):
    permission_classes = [IsAuthenticated]
    serializer_class = PhlebotomistSerializer

    def get_queryset(self):
        return Phlebotomist.objects.filter(Shop=self.request.user.shop)


class OrderServiceViewSet(BaseClass):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderServiceSerializer

    def get_queryset(self):
        return OrderService.objects.filter(Order__complete=True, PathologicalTestService__Shop=self.request.user.shop)


class PathoOrdersViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PathoOrdersSerializer

    def get_queryset(self):
        return OrderService.objects.filter(Order__paymentDone=True,
                                           PathologicalTestService__Shop=self.request.user.shop)


class PathologicalTestServiceViewset(BaseClass):
    permission_classes = [IsAuthenticated]
    serializer_class = PathologicalTestServiceSerializer

    def get_queryset(self):
        return Pathological_Test_Service.objects.filter(Shop=self.request.user.shop)
