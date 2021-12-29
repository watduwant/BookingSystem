from auth_app.models import User
from django.contrib.auth.decorators import login_required
from store.models import ServiceDetailsDay, Shop, ServiceDetailsDayTime, Service, Doctor
from django.shortcuts import render, redirect
from .models import Appointment
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

        return render(request, 'customer/index.html',
                      {'shops': shops, 'today': today, 'searched': searched, 'searches': searches, 'search': search, })

    else:
        return render(request, 'customer/index.html', {'shops': shops, 'today': today})



def btnchk(request):
    if request.user.is_authenticated:
        return render(request, 'customer/index.html')
    else:
        return render(request, 'sign-up.html')


@login_required(login_url='login')
def account(request):
    profile = User.objects.get(id=request.user.id)
    appointments = Appointment.objects.filter(Customer=request.user)
    return render(request, 'customer/account.html', {'profile': profile, 'appointments': appointments})


def show_details(request, shop_id):
    details = Shop.objects.get(pk=shop_id)
    data = Service.objects.filter(Clinic=details) 
   # data1 = ServiceDetailsDayTime.objects.get(pk=ServiceDetailsDayID)
  # data1 = ServiceDetailsDayTime.objects.all().select_related("ServiceDetailsDay")

    return render(request, 'clinicalldetails.html', {'details': details, 'data': data})


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
            # date = request.POST.get("date").split(",")
            # datefm = datetime.date(int(date[2]), int(date[1]), int(date[0]))
            day = request.POST.get("days")
            timelist = request.POST.get("Time").split(",")
            time = timelist[0]
            time2 = timelist[1]
            status = "P"
            time2 = datetime.datetime.strptime(time2, '%H:%M:%S').time()
            slots = ServiceDetailsDayTime.objects.get(
                ServiceDetailsDayID__ServiceID=service_pk, Time=time2).Visit_capacity
            Nslots = Appointment.objects.filter(Status="P", Service__ServiceDetailsDayID__ServiceID=service, day=day, time=time).count(
            ) + Appointment.objects.filter(Status="A", Service__ServiceDetailsDayID__ServiceID=service, day=day, time=time).count()

            if(Nslots+1 > slots):
                messages.error(
                    request, "No slots are available on that date. Please choose a different date!!")
                return redirect(f'../show_details/{shop_id}')

            servicedetaildaytime = ServiceDetailsDayTime.objects.get(ServiceDetailsDayID__ServiceID=service)
            appointment = Appointment(Customer=customer,Service=servicedetaildaytime, PatientName=patient_name,
                                      Age=age, Sex=sex, Status=status, phone=phone, day=day, time=time)
            appointment.save()
            messages.success(
                request, "Your request has been received and we'll notify you shortly about the confirmation.")
            return redirect(f'../show_details/{shop_id}')
        messages.error(request, "Fill the appointment form correctly.")
        return redirect("customer-home")
    messages.error(request, "You must login to book an appointment.")
    return redirect("customer-home")
