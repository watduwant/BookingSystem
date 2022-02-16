from posixpath import basename
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ShopViewSet, UserViewSet, DoctorViewSet, ServiceViewSet, ServicedetailDayViewSet,ServicedetailDayTimeViewSet, AppointmentViewSet, HomeScreenViewset, ViewDoctorViewset

router = DefaultRouter()
router.register('shops', ShopViewSet, basename='shops')

router.register('users', UserViewSet, basename='users')
router.register('doctors', DoctorViewSet, basename='doctors')
router.register('services', ServiceViewSet, basename='services')
router.register('servicedetailsday', ServicedetailDayViewSet, basename='servicedetailsday')
router.register('viewdoctors', ViewDoctorViewset, basename='view-doctors')
# router.register('home', HomeScreenViewset, basename='homescreen')
router.register('servicedetailsdaytime', ServicedetailDayTimeViewSet, basename='servicedetailsdaytime')
router.register('appointments', AppointmentViewSet, basename='appointment')


urlpatterns = [
               path('', include(router.urls)),
               path('home/', HomeScreenViewset.as_view(), name="homescreen")

             ]