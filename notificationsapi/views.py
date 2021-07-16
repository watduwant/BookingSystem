# Create your views here.
# from django.db.models import Q
from fcm_django.api.rest_framework import DeviceViewSetMixin, FCMDeviceSerializer
from fcm_django.models import FCMDevice
# from notificationsapi.permissions import IsAdminUser
# from requests import Response
# from rest_framework.request import Request
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# from .serializers import StockTipsSerializer, GenericNotificationSerializer
# from .models import StockTip, GenericNotification
# from rest_framework import viewsets
# from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet


#Ifl Services ViewSets
# class IflServicesStockTipsViewSet(viewsets.ModelViewSet):
#     queryset = StockTip.objects.all().order_by('-id')
#     serializer_class = StockTipsSerializer

#     # Permissions
#     def get_permissions(self):
#         permission_classes = []
#         if self.action == 'create':
#             permission_classes = [IsAdminUser]
#         elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
#             permission_classes = [IsAdminUser]
#         elif self.action == 'list':
#             permission_classes = [AllowAny]
#         elif self.action == 'destroy':
#             permission_classes = [IsAdminUser]
#         return [permission() for permission in permission_classes]

# class IflServicesGenericNotificationViewSet(viewsets.ModelViewSet):
#     queryset = GenericNotification.objects.filter(created_by__profile__belongs_to="ifl_services").order_by('-id')
#     serializer_class = GenericNotificationSerializer

#     # Permissions
#     def get_permissions(self):
#         permission_classes = []
#         if self.action == 'create':
#             permission_classes = [IsAdminUser]
#         elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
#             permission_classes = [IsAdminUser]
#         elif self.action == 'list':
#             permission_classes = [AllowAny]
#         elif self.action == 'destroy':
#             permission_classes = [IsAdminUser]
#         return [permission() for permission in permission_classes]


# #Equity Global ViewSets
# class EquityGlobalStockTipsViewSet(viewsets.ModelViewSet):
#     queryset = StockTip.objects.filter(created_by__profile__belongs_to="EquityGlobal").order_by('-id')
#     serializer_class = StockTipsSerializer

#     # Permissions
#     def get_permissions(self):
#         permission_classes = []
#         if self.action == 'create':
#             permission_classes = [IsAdminUser]
#         elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
#             permission_classes = [IsAdminUser]
#         elif self.action == 'list':
#             permission_classes = [AllowAny]
#         elif self.action == 'destroy':
#             permission_classes = [IsAdminUser]
#         return [permission() for permission in permission_classes]


# class EquityGlobalGenericNotificationViewSet(viewsets.ModelViewSet):
#     queryset = GenericNotification.objects.filter(created_by__profile__belongs_to="EquityGlobal").order_by('-id')
#     serializer_class = GenericNotificationSerializer

#     # Permissions
#     def get_permissions(self):
#         permission_classes = []
#         if self.action == 'create':
#             permission_classes = [IsAdminUser]
#         elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
#             permission_classes = [IsAdminUser]
#         elif self.action == 'list':
#             permission_classes = [AllowAny]
#         elif self.action == 'destroy':
#             permission_classes = [IsAdminUser]
#         return [permission() for permission in permission_classes]




#Common ViewSets
#Custom FCM ViewSets & Mixins
class AuthorizedMixin(object):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )


    def get_queryset(self):
        # filter all devices to only those belonging to the current user
        return self.queryset.filter(user=self.request.user)


class FCMDeviceViewSet(DeviceViewSetMixin, ModelViewSet):
    queryset = FCMDevice.objects.all()
    serializer_class = FCMDeviceSerializer


class FCMDeviceAuthorizedViewSet(AuthorizedMixin, FCMDeviceViewSet):
    pass
