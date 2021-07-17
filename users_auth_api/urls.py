from .views import UserSubscriptionViewSet, UserViewSet, UserSubscribedViewSet, UserStockPermissionsViewSet
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('users_subscription', UserSubscriptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user-trial-period/', UserSubscribedViewSet, name="user-trial-period"),
    path('user-stock-permissions/', UserStockPermissionsViewSet, name="user-stock-permissions")
]