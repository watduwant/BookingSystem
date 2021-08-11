from .views import home, clinic_details, account
from django.urls import path
urlpatterns = [
        path('',home,name='customer-home'),
        path('account', account,name='account'),
        path('clinic-details/<int:id>', clinic_details, name="clinic-details")
        ]
