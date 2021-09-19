from .views import home, clinic_details, account
from django.urls import path
from customer import views

urlpatterns = [
        path('',home,name='customer-home'),
        path('account', account,name='account'),
        # path('clinic-details/<int:id>', clinic_details, name="clinic-details")
        path('clinicalldetails', clinic_details, name="clinic-details"),
        path('search_result', views.search_result, name='search_result'),
        path('show_details/<shop_id>', views.show_details, name='show_details'),
        # path('list', views.all_list, name='clinic_list'),
        ]
