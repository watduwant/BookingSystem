from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ShopViewSet, UserViewSet, ProfileViewSet, DoctorViewSet, ServicedetailViewSet, ServiceViewSet, AppointmentViewSet

router = DefaultRouter()
router.register('shops', ShopViewSet, basename='shops')
router.register('profiles', ProfileViewSet, basename='profiles')
router.register('users', UserViewSet, basename='users')
router.register('doctors', DoctorViewSet, basename='doctors')
router.register('services', ServiceViewSet, basename='services')
router.register('servicedetails', ServicedetailViewSet, basename='servicedetails')
router.register('appointments', AppointmentViewSet, basename='appointment')


urlpatterns = [
               path('', include(router.urls))
               #  path('dj-rest-auth/', include('dj_rest_auth.urls')),
               #  path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
             ]