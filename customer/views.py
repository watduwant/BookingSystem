from django.contrib.auth.decorators import login_required
from store.models import ServiceDetails, Shop
from django.shortcuts import render, redirect
from .models import Appointment
from store.models import Service, Doctor
from datetime import datetime
# Create your views here.
        

@login_required(login_url='login')
def home(request):
    shops = Shop.objects.all()
    today = datetime.today().weekday()
    context={
        'shops': shops,
        'today': today,
    }
    return render(request,'customer/index.html',context)

@login_required(login_url='login')
def account(request):
    return render(request,'customer/account.html')








def show_details(request, shop_id):
    details = Shop.objects.get(pk=shop_id)
    print(datetime.today().weekday())
    data = Service.objects.filter(Clinic=details)
    # servicedetails = ServiceDetails.objects.filter(ServiceID = data)
    # data1 = Doctor.objects.all()

    return render(request, 'clinicalldetails.html', {'details': details, 'data': data, })

# def all_list(request):
#     cliniclist = Shop.objects.all()
#     return render(request, 'cliniclist.html', {'cliniclist': cliniclist})



def search_result(request):
    if request.method == "POST":
        searched = request.POST['searched']
        searches = Doctor.objects.filter(Name__icontains=searched)
        search = Shop.objects.filter(Name__icontains=searched)

        return render(request, 'search_result.html', {'searched': searched,
                                                      'searches': DoctorSerializer(searches, many=True).data, 'search': ShopSerializer(search, many=True).data})

    else:
        return render(request, 'search_result.html', {})









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
            print(sex)
            status = "P"
            appointment = Appointment(Customer=customer, Service=service, PatientName=patient_name, Age=age, Sex=sex, Status=status, phone=phone)
            appointment.save()
        return redirect('customer-home')
    return redirect("appointment")


