from auth_app.models import Profile
from django.contrib.auth.decorators import login_required
from store.models import ServiceDetails, Shop
from django.shortcuts import render, redirect
from .models import Appointment
from store.models import Service, Doctor
import datetime
# Create your views here.
        

@login_required(login_url='login')
def home(request):
    shops = Shop.objects.all()
    today = datetime.datetime.today().weekday()
    context={
        'shops': shops,
        'today': today,
    }
    return render(request,'customer/index.html',context)

@login_required(login_url='login')
def account(request):
    profile = Profile.objects.get(user=request.user)
    appointments = Appointment.objects.filter(Customer = request.user)
    return render(request,'customer/account.html', {'profile': profile, 'appointments': appointments})



def show_details(request, shop_id):
    details = Shop.objects.get(pk=shop_id)
    date = datetime.date.today() + datetime.timedelta(days=5)
    print(date )
    data = Service.objects.filter(Clinic=details)

    return render(request, 'clinicalldetails.html', {'details': details, 'data': data, })



def search_result(request):
    if request.method == "POST":
        searched = request.POST['searched']
        searches = Doctor.objects.filter(Name__icontains=searched)
        search = Shop.objects.filter(Name__icontains=searched)

        return render(request, 'search_result.html', {'searched': searched,
                                                      'searches': DoctorSerializer(searches, many=True).data, 'search': ShopSerializer(search, many=True).data})

    else:
        return render(request, 'search_result.html', {})


def appointment(request):
    rank_alloted = Appointment.objects.filter(Status="P")
    if request.user.is_authenticated:
        if request.method == "POST":
            customer = request.user
            service_pk = request.POST.get("service_pk")
            service = Service.objects.get(pk=service_pk)
            patient_name = request.POST.get("patient_name")
            age = request.POST.get("age")
            phone = request.POST.get("phone")
            sex = request.POST.get("sex")
            date = request.POST.get("date").split(",")
            # print(request.POST.get("date"))
            datefm = datetime.date(int(date[2]), int(date[1]), int(date[0]) )
            time = request.POST.get("time")
            print(datefm)
            status = "P"
            appointment = Appointment(Customer=customer, Service=service, PatientName=patient_name, Age=age, Sex=sex, Status=status, phone=phone, date=datefm, time=time)
            appointment.save()
        return redirect('customer-home')
    return redirect("appointment")


