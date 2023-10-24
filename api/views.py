from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import Token
from rest_framework.exceptions import APIException
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
    RegisterUserSerializer,
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
    AppointmentListSerializer,
    UserInfoSerializer
)
from .static_variables import USER_STATUS


# Create your views here.

class BaseClass(ModelViewSet):
    class CustomAPIException(APIException):
        status_code = 400
        default_detail = 'You are not authorized to access this endpoint'

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        data = {
            "count": len(serializer.data),
            "data": serializer.data,
        }
        return Response(data)


class UserLogin(APIView):
    http_method_names = ['post']

    def post(self, request):
        try:
            request = request.data
            user = ""
            if request:
                if request.get('email'):
                    email = request.get('email')
                    user = User.objects.filter(email=email).first()
                if request.get('mobile'):
                    mobile = request.get('mobile')
                    user = User.objects.filter(mobile=mobile).first()
                if user.check_password(request.get('password')):
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({
                        'token': token.key,
                        'user_id': user.pk,
                        'mobile': user.mobile.national_number
                    })
            else:
                return Response({
                    "email/mobile": "NULL",
                    "password": "NULL"
                })
        except Exception as err:
            return Response({
                "error": "you provided credential is not valid!!",
            })


class ShopAppointmentViewSet(BaseClass):
    http_method_names = ['get']
    queryset = Appointment.objects.all()
    serializer_class = AppointmentListSerializer

    def get_queryset(self):
        try:
            if self.request.user.status == USER_STATUS.CR:
                raise
            if self.request.user.status == USER_STATUS.SO:
                return self.queryset.filter(Service__ServiceDetailsDayID__ServiceID__Clinic__Shop_owner=self.request.user)
        except:
            raise self.CustomAPIException()


class UserAppointmentViewSet(BaseClass):
    http_method_names = ['get']
    queryset = Appointment.objects.all()
    serializer_class = AppointmentListSerializer

    def get_queryset(self):
        return self.queryset.filter(appointment_user=self.request.user.id)


class ShopViewSet(BaseClass):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_anonymous:
            if user.is_superuser:
                return self.queryset.filter(Shop_owner__status=USER_STATUS.SO)
            if self.action == 'list':
                queryset = Shop.objects.filter(Shop_owner__email=self.request.user.email)
            if self.action == 'retrieve':
                queryset = Appointment.objects.filter(appointment_user=self.request.user)
        else:
            raise self.CustomAPIException()
        return queryset

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
    queryset = ServiceDetailsDay.objects.all()

    class CustomAPIException(APIException):
        status_code = 400
        default_detail = 'You are not the shop owner or associated with any shop'

    def get_queryset(self):
        user = self.request.user
       
        service_id = self.request.query_params.get('service_id', None)
        if user.status == USER_STATUS.SO:
            clinic = Shop.objects.get(Shop_owner =user)   
            if service_id:
                return ServiceDetailsDay.objects.filter(ServiceID__id=service_id)
            # return ServiceDetailsDay.objects.filter(ServiceID__Clinic=user.shop_user).order_by('ServiceID')
            return ServiceDetailsDay.objects.filter(ServiceID__Clinic=clinic) #ServiceDetailsDay.objects.all()
        else:
            raise self.CustomAPIException()


class AppointmentViewSet(BaseClass):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()

    # def get_queryset(self):
    #     queryset = Appointment.objects.all()
    #     if self.action == 'list':
    #         queryset = Appointment.objects.filter(appointment_user=self.request.user)
    #     if self.action == 'retrieve':
    #         queryset = Appointment.objects.filter(appointment_user=self.request.user)
    #     return queryset

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


class RegisterUserViewSet(BaseClass):
    http_method_names = ['post']
    queryset = User.objects.exclude(is_superuser=True)
    serializer_class = RegisterUserSerializer


class UserViewSet(BaseClass):
    http_method_names = ['get']
    queryset = User.objects.exclude(is_superuser=True)
    serializer_class = UserInfoSerializer

    class CustomAPIException(APIException):
        status_code = 400
        default_detail = 'You are not Authorized to access this endpoint'

    class payloadAPIException(APIException):
        status_code = 400
        default_detail = 'Please provide valid data'

    def get_queryset(self):

        if self.request.data:
            request = self.request.data
            if request.get('user_id') and not request.get('mobile'):
                return User.objects.exclude(is_superuser=True).filter(
                    id=request.get('user_id')
                )
            if request.get('mobile') and not request.get('user_id'):
                return User.objects.exclude(is_superuser=True).filter(
                    mobile=request.get('mobile')
                )
            if request.get('user_id') and request.get('mobile'):
                query = User.objects.exclude(is_superuser=True).filter(id=request['user_id'], mobile=request['mobile'])
                if query:
                    return query
                else:
                    raise self.payloadAPIException()
        if not self.request.user.is_anonymous:
            return User.objects.exclude(is_superuser=True)
        else:
            raise self.CustomAPIException()


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
            return Response({"error": "You are not the shop owner or associated with any shop"})


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
