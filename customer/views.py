from ast import Try
from auth_app.models import User
from django.contrib.auth.decorators import login_required
from store.models import ServiceDetailsDay, Shop, ServiceDetailsDayTime, Service, Doctor, OrderService, Pathological_Test_Service, Cart, Order
from django.shortcuts import render, redirect
from .models import Appointment
from django.contrib import messages
import datetime
import json
import razorpay
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
import os
 
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


def showCart(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    price = 0
    for item in cart.orderServices.all():
        price += item.PathologicalTestService.Price*item.quantity
    cart.total_price = price
    cart.save()
    id = 1
    for item in cart.orderServices.all():
        id = item.id
    
    client = razorpay.Client(auth=("rzp_test_wjZAp6QdWONwih", "VWWSovCkW3DMdqs1tkLm70tx"))
    if price == 0: 
        price = 1
    DATA = {
        "amount": price*100,
        "currency": "INR",
        "payment_capture": "1",
        # "receipt": "receipt#1",
        # "notes": {
        #     "key1": "value3",
        #     "key2": "value2"
        # }
    }
    # client.order.create(data=DATA)
    payment = client.order.create(data=DATA)

    return render(request, "customer/cart.html", {'cart': cart, 'user': request.user, 'payment': payment, 'amount': price*100})


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

    return render(request, 'clinicalldetails.html', {'details': details, 'data': data, 'n':range(2)})

def serviceTime(request):
    dayID = request.GET.get("dayId");
    serviceTimes = ServiceDetailsDay.objects.get(id=dayID).serviceDetailsDayTimes.all
    # serviceTimes = serviceTimes.serviceDetailsDayTimes.all()
    return render(request, 'serviceTimeDropdown.html', {'serviceTimes': serviceTimes})


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

            day = request.POST.get("days")
            timelist = request.POST.get("Time").split(",")
            time = timelist[0]
            time2 = timelist[1]
            status = "P"
            time2 = datetime.datetime.strptime(time2, '%H:%M:%S').time()
            serviceday = ServiceDetailsDay.objects.get(Day=day, ServiceID=service_pk)
            slots = ServiceDetailsDayTime.objects.get(
                ServiceDetailsDayID=serviceday, Time=time2).Visit_capacity
            Nslots = Appointment.objects.filter(Status="P", Service__ServiceDetailsDayID__ServiceID=service, day=day, time=time).count(
            ) + Appointment.objects.filter(Status="A", Service__ServiceDetailsDayID__ServiceID=service, day=day, time=time).count()

            if(Nslots+1 > slots):
                messages.error(
                    request, "No slots are available on that date. Please choose a different date!!")
                return redirect(f'../show_details/{shop_id}')

            servicedetaildaytime = ServiceDetailsDayTime.objects.get(ServiceDetailsDayID__ServiceID=service_pk, Time=time2)
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


def BookPathologicalService(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user = request.user
            patient_name = request.POST['patient_name']
            age = request.POST.get("age")
            phone = request.POST.get("phone")
            sex = request.POST.get("sex")
            pathological_pk = request.POST["pathological_pk"]
            pathologicalTestService = Pathological_Test_Service.objects.get(id=pathological_pk)
            shop_id = pathologicalTestService.Shop.id
            cart = Cart.objects.get(user=user)
            orderService = OrderService(Cart=user.cart, PathologicalTestService=pathologicalTestService)
            orderService.save()
            cart.total_price =  cart.total_price + pathologicalTestService.Price*orderService.quantity
            cart.save()

            messages.success(
                request, "Your request has been received and we'll notify you shortly about the confirmation.")
            return redirect(f'../show_details/{shop_id}')
        messages.error(request, "Fill the booking form correctly.")
        return redirect("customer-home")
    messages.error(request, "You must login to book an appointment.")
    return redirect("customer-home")

def updateAddress(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user = request.user
            city = request.POST['city']
            address = request.POST.get("address")
            flat_name = request.POST.get("flat_name")
            landmark = request.POST.get("landmark")
            pincode = request.POST.get("pincode")
            user.city = city
            user.address = address
            user.flat_name = flat_name
            user.landmark = landmark
            user.pincode = pincode
            user.save()

            messages.success(
                request, "You have successfully updated your address.")
            return redirect(f'../cart')
        messages.error(request, "Fill the address form correctly.")
        return redirect("customer-home")
    messages.error(request, "You must login to update Address.")
    return redirect("customer-home")

@csrf_exempt
def paymentHandler(request):
    if request.method == "POST":

        cart = request.user.cart
        price = cart.total_price

        order = Order.objects.create(user=request.user, total_price = price)

        # order.save()
        for item in cart.orderServices.all():
            order.orderServices.add(item)

        order.save()
        cart.orderServices.clear()
        cart.save()

        return render(request, 'customer/payment_succesful.html')
    

    # def success(request):





