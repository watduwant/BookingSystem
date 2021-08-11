from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from store.models import Shop
# Create your views here.
        

@login_required(login_url='login')
def home(request):
    shops = Shop.objects.all()
    context={
        'shops': shops
    }
    return render(request,'customer/index.html',context)

@login_required(login_url='login')
def account(request):
    return render(request,'customer/account.html')

@login_required(login_url='login')
def clinic_details(request, id):
    shops = Shop.objects.all()
    context={
        'shops': shops
    }

    return render(request, "customer/clinic-details.html", context)