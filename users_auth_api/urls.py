from .views import UserViewSet, \
    UserSubscribedViewSet, \
    UserStockPermissionsViewSet
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('sensex-nifty-data/', SensexNiftyView, name="sensex-nifty-data"),
    path('user-trial-period/', UserSubscribedViewSet, name="user-trial-period"),
    path('user-stock-permissions/', UserStockPermissionsViewSet, name="user-stock-permissions")
]