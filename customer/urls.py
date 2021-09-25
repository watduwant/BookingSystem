from .views import home, account
from django.urls import path
from customer import views

urlpatterns = [
        path('',home,name='customer-home'),
        path('account', account,name='account'),
        path('search_result', views.search_result, name='search_result'),
        path('show_details/<shop_id>', views.show_details, name='show_details'),
        # path('list', views.all_list, name='clinic_list'),
        ]
