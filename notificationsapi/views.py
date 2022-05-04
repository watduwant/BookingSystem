# Create your views here.
from fcm_django.api.rest_framework import DeviceViewSetMixin, FCMDeviceSerializer
from fcm_django.models import FCMDevice
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


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
