"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import imp
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
# from rest_framework.authtoken.views import obtain_auth_token
# from auth_app.views import ObtainAuthToken
from auth_app.views import obtain_auth_token
from customer.views import appointment


urlpatterns = [
                path('appointment', appointment, name="appointment"),
                path('', include('auth_app.urls'),name='auth'),
                path('admin/', admin.site.urls),    
                path('',include('customer.urls'),name='customer'),
                path('store/',include('store.urls'),name='store'),
                path('api/auth', obtain_auth_token,name='auth'),
                path('api/',include('api.urls'),name='api'),
                path('accounts/', include('allauth.urls')),
                # path('api-auth/', include('rest_framework.urls')),
                # path('api/dj-rest-auth/', include('dj_rest_auth.urls')),
                #path('api/dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
             ]

urlpatterns += static(settings.STATIC_URL , document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)
