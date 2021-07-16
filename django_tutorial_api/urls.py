"""django_tutorial_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from .reset_password_view.views import PasswordResetConfirmView, PasswordResetView
from notificationsapi.views import FCMDeviceAuthorizedViewSet
from django.contrib.auth import views as auth_view
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Django Tutorial Admin Portal"
admin.site.site_title = "Django Tutorial Admin Portal"
admin.site.index_title = "Welcome to Django Tutorial Admin Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users_auth_api.urls')),
    # path('stockstips/', include('chloral_api.urls')),
    # path('stocksdata/', include('stocksdata.urls')),
    # path('ohlcdata/', include('ohlc_data.urls')),
    # path('reserch_and_daily_profit_loss_report/', include('reserch_and_daily_profit_loss_report.urls')),
    # path('stocktips/', include('stocktips_crawler.urls')),
    path('youtubevideos/', include('youtube_videos.urls')),
    path('api/notifications/', include('notificationsapi.urls')),
    # path('api/assets/', include('assets_api.urls')),
    # path('api/stocks/', include('stocks_api.urls')),
    path('devices/', FCMDeviceAuthorizedViewSet.as_view({'post': 'create'}),
         name='create_fcm_device'),

    #Auth Urls
    path('auth/password/reset/', PasswordResetView.as_view(),
        name='rest_password_reset'),
    path('auth/', include('rest_auth.urls')),
    path('reset/<uidb64>/<token>/<app_source>', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_view.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
