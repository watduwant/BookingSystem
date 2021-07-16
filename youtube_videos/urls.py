from django.urls import path, include
from rest_framework import routers
from .views import HtmlVideosViewSet, CssVideoViewSet, PythonVideoViewSet, JavaScriptVideoViewSet, DjangoVideoViewSet, AngularVideoViewSet, AngularProjectVideoViewSet, DjangoProjectVideoViewSet

router = routers.DefaultRouter()
router.register('htmlvideos', HtmlVideosViewSet)
router.register('cssvideos', CssVideoViewSet)
router.register('pythonvideos', PythonVideoViewSet)
router.register('javascriptvideos', JavaScriptVideoViewSet)
router.register('djangovideos', DjangoVideoViewSet)
router.register('angularvideos', AngularVideoViewSet)
router.register('djangoprojectvideos', DjangoProjectVideoViewSet)
router.register('angularprojectvideos', AngularProjectVideoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]