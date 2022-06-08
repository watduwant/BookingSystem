from django.urls import path, include
from rest_framework.routers import DefaultRouter


from pathological_test.views import PathologicalTestViewSet, PathologicalTestDetailsViewSet, ShopingCartViewSet, GetShopingCartViewSet, OrderDetailViewSet, UserOrderViewSet, PhlebotomistsViewSet, ClinicViewSet, ClinicDoctorViewSet


router = DefaultRouter()
router.register('all_clinic_test', PathologicalTestDetailsViewSet, basename='all_clinic_test')
router.register('clinic', ClinicViewSet, basename='clinic')
router.register('doctor', ClinicDoctorViewSet, basename='clinic_doctors')
router.register('list_of_test', PathologicalTestViewSet, basename='list_of_test')
router.register('shoping_cart', ShopingCartViewSet, basename='shoping_cart')  
router.register('get_shoping_cart', GetShopingCartViewSet, basename='get_shoping_cart')
router.register('order_details', OrderDetailViewSet, basename='order_details')
router.register('user_order', UserOrderViewSet, basename='user_order')
router.register('phlebotomists', PhlebotomistsViewSet, basename='phlebotomists')

# pathological/all_clinic_test/filter_by_clinic/?clinic_id=2
urlpatterns = [
               path('', include(router.urls)),
             ]