from posixpath import basename
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ShopViewSet, UserViewSet, DoctorViewSet, ServiceViewSet, ServicedetailDayViewSet,ServicedetailDayTimeViewSet, AppointmentViewSet, HomeScreenViewset, ViewDoctorViewset, phlebotomistViewset, OrderServiceViewSet, PathoOrdersViewSet, PathologicalTestServiceViewset

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
router.register('phlebotomist', phlebotomistViewset, basename='phlebotomist')
router.register('order-services', OrderServiceViewSet, basename='order-services')
router.register('patho-orders', PathoOrdersViewSet, basename='patho-orders')
router.register('pathoTests', PathologicalTestServiceViewset, basename='pathoTests')


urlpatterns = [
               path('', include(router.urls)),
               path('home/', HomeScreenViewset.as_view(), name="homescreen")

             ]