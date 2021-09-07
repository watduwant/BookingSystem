from django.contrib.auth.decorators import login_required
from store.models import Shop
from django.shortcuts import render, redirect
from .models import Appointment
from store.models import Service
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

# @login_required(login_url='login')
# def clinic_details(request, id):
#     shops = Shop.objects.all()
#     context={
#         'shops': shops
#     }

#     return render(request, "customer/clinic-details.html", context)

@login_required(login_url='login')
def clinic_details(request):
    shops = Shop.objects.all()
    context={
        'shops': shops
    }

    return render(request, "customer/clinicalldetails.html", context)

def appointment(request):
    rank_alloted = Appointment.objects.filter(status="P")
    if request.user.is_authenticated:
        if request.method == "POST":
            customer = request.user
            service_pk = request.POST.get("service_pk")
            service = Service.objects.get(pk=service_pk)
            patient_name = request.POST.get("patient")
            age = request.POST.get("age")
            sex = request.POST.get("sex")
            status = "P"
            rank_alloted = Appointment.objects.filter(Status="P", Service=service).count() + Appointment.objects.filter(Status="A", Service=service).count()
            appointment = Appointment(Customer=customer, Service=service, PatientName=patient_name, Age=age, Sex=sex, Status=status)
            appointment.Rank = rank_alloted + 1
            appointment.save()
        return redirect('home')
    return redirect("appointment")


