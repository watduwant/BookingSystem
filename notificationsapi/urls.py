from .views import  FCMDeviceAuthorizedViewSet
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

#Common Urls
router.register('list/devices', FCMDeviceAuthorizedViewSet)


urlpatterns = [
    path('', include(router.urls)),
]