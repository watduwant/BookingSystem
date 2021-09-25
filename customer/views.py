from auth_app.models import Profile
from django.contrib.auth.decorators import login_required
from store.models import ServiceDetails, Shop
from django.shortcuts import render, redirect
from .models import Appointment
from store.models import Service, Doctor
from django.contrib import messages
import datetime
# Create your views here.
        



def home(request):
    shops = Shop.objects.all()
    today = datetime.datetime.today().weekday()

    if request.method == "POST":
        searched = request.POST['searched']

        searches = Doctor.objects.filter(Name__icontains=searched)
        search = Shop.objects.filter(Name__icontains=searched)

        return render(request, 'customer/index.html',  {'shops': shops, 'today': today, 'searched': searched, 'searches': searches, 'search': search, })

    else:
        return render(request, 'customer/index.html', {'shops': shops, 'today': today})

def btnchk(request):
    if request.user.is_authenticated:
        return render(request, 'customer/index.html')
    else:
        return render(request, 'sign-up.html')


@login_required(login_url='login')
def account(request):
    profile = Profile.objects.get(user=request.user)
    appointments = Appointment.objects.filter(Customer = request.user)
    return render(request,'customer/account.html', {'profile': profile, 'appointments': appointments})



def show_details(request, shop_id):
    details = Shop.objects.get(pk=shop_id)
    data = Service.objects.filter(Clinic=details)

    return render(request, 'clinicalldetails.html', {'details': details, 'data': data, })



def search_result(request):

    if request.method == "POST":
        searched = request.POST['searched']

        searches = Doctor.objects.filter(Name__icontains=searched)
        search = Shop.objects.filter(Name__icontains=searched)

        return render(request, 'search_result.html', {
            'searched': searched,
            'searches': searches, 'search': search})

    else:
        return render(request, 'search_result.html', {})

def appointment(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            customer = request.user
            service_pk = request.POST.get("service_pk")
            service = Service.objects.get(pk=service_pk)
            patient_name = request.POST.get("patient_name")
            shop_id = service.Clinic.id
            age = request.POST.get("age")
            phone = request.POST.get("phone")
            sex = request.POST.get("sex")
            date = request.POST.get("date").split(",")
            datefm = datetime.date(int(date[2]), int(date[1]), int(date[0]) )
            time = request.POST.get("time")
            status = "P"
            appointment = Appointment(Customer=customer, Service=service, PatientName=patient_name, Age=age, Sex=sex, Status=status, phone=phone, date=datefm, time=time)
            appointment.save()
            messages.success(request, "Your request has been received and we'll notify you shortly about the confirmation.")
            return redirect(f'../show_details/{shop_id}')
        messages.ERROR(request, "Fill the appointment form correctly.")
        return redirect("customer-home")
    messages.ERROR(request, "Fill the appointment form correctly.")
    return redirect("customer-home")


