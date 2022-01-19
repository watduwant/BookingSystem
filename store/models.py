from django.db import models
from auth_app.models import User

# Create your models here.
week_days = (
    ('1', 'Monday'),
    ('2', 'Tuesday'),
    ('3', 'Wednesday'),
    ('4', 'Thursday'),
    ('5', 'Friday'),
    ('6', 'Saturday'),
    ('7', 'Sunday')
)


class Shop(models.Model):
    shop_status = (
        ('E', 'ENABLE'),
        ('D', 'DISABLE')
    )
    Name = models.CharField(max_length=190, unique=True)
    Shop_owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    Address = models.CharField(max_length=300)
    Status = models.CharField(max_length=2, choices=shop_status, default='E')
    Interior_image = models.ImageField(
        upload_to='shops', blank=True, null=True)
    OffDay = models.CharField(max_length=10, default="7", choices=week_days)
    Image = models.ImageField(upload_to='shops', blank=True, null=True)
    Opening_time = models.TimeField(null=True, blank=True)
    Closing_time = models.TimeField(null=True, blank=True)
    Shop_url = models.URLField(
        max_length=200, default='www.watduwant.com/show_details')

    def __str__(self):
        return self.Name

    def save(self, *args, **kwargs):
        if self.Shop_url and len(self.Shop_url.split('-')) > 1:

            self.Shop_url = self.Shop_url.split('-')[1]

            self.Shop_url = '{}/{}'.format(self.Shop_url, self.Name,)

        super(Shop, self).save(*args, **kwargs)


class Pathological_Test(models.Model):
    TestName = models.CharField(max_length=100)
    Desc =  models.TextField()
    Image = models.ImageField(upload_to='shops', blank=True, null=True)
    SampleType  = models.CharField(max_length=100)
    FastingRequirement = models.BooleanField(default=False)

    def __str__(self):
        return self.TestName


class Pathological_Test_Service(models.Model):
    Shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="PathologicalTestServices")
    Tests = models.ForeignKey(Pathological_Test, on_delete=models.CASCADE, related_name="PathologicalTestServices")
    Price = models.IntegerField()
    ReportDeliveryTime = models.TimeField()

    def __str__(self):
        return f"{str(self.Shop)} - {str(self.Tests)}"
    


class Doctor(models.Model):
    Name = models.CharField(max_length=100, unique=True)
    Specialization = models.CharField(max_length=200, blank=False)
    Experience = models.IntegerField()
    Image = models.ImageField(upload_to='doctors', blank=True, null=True)

    def __str__(self):
        return self.Name

class Phlebotomist(models.Model):
    Shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="Phlebotomists")
    Name = models.CharField(max_length=100)
    PhoneNumber = models.CharField(max_length=15)


class Order(models.Model):
    User =  models.OneToOneField(User, on_delete=models.CASCADE, related_name="Order")
    DateOrdered = models.DateField()
    complete = models.BooleanField(default=False)
    transactionId = models.CharField(max_length=12)

    def __str__(self):
        return self.User + " - Order" 

class OrderService(models.Model):
    Order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderServices")
    PathologicalTestService = models.ForeignKey(Pathological_Test_Service, on_delete=models.CASCADE, related_name="pathologicalTestServices")
    DateAdded = models.DateField(auto_now_add=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.Order + " - " + self.quantity

Gender_Choices  = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)

class ShippingAddress(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shippingAddresses")
    patientName = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(choices=Gender_Choices, max_length=5)
    FlatName = models.CharField(max_length=200)
    StreetName = models.CharField(max_length=200)
    pincode =  models.CharField(max_length=10)
    AddressType = models.CharField(max_length=200)
    MobileNumber = models.CharField(max_length=15)
    AppointmentDate = models.DateField()
    AppointmentTimeSlot = models.TimeField()

    def __str__(self):
        return self.User + " - " + self.patientName
    



class Service(models.Model):
    Clinic = models.ForeignKey(
        Shop, on_delete=models.CASCADE, null=True, blank=True)
    Doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, null=True, blank=True)
    Fees = models.IntegerField()

    class Meta:
        unique_together = (('Clinic', 'Doctor'),)

    @property
    def get_name(self):
        return self.Clinic.Name + "--" + self.Doctor.Name

    def __str__(self):
        return self.get_name


class ServiceDetailsDay(models.Model):
    ServiceID = models.ForeignKey(
        Service, on_delete=models.CASCADE, null=True, blank=True, related_name='serviceDetailsDays')
    Day = models.CharField(max_length=10, choices=week_days, null=True)

    class Meta:
        unique_together = (('ServiceID', 'Day'),)

    @property
    def get_name_day(self):
        return self.ServiceID.get_name + "--" + str(self.Day)

    def __str__(self):
        return self.get_name_day


class ServiceDetailsDayTime(models.Model):
    ServiceDetailsDayID = models.ForeignKey(
        ServiceDetailsDay, on_delete=models.CASCADE, null=True, blank=True, related_name='serviceDetailsDayTimes')
    Time = models.TimeField()
    Visit_capacity = models.IntegerField()

    class Meta:
        unique_together = (('ServiceDetailsDayID', 'Time'),)

    @property
    def get_service_id(self):
        return self.ServiceDetailsDayID.ServiceID.id

    def __str__(self):
        return self.ServiceDetailsDayID.get_name_day + "--" + str(self.Time)


'''
***
###


    - Add field day to servicedetails
    - Alter unique_together for service (1 constraint(s))       
    - Alter unique_together for servicedetails (1 constraint(s))
    - Remove field day from service
    - Remove field Time from servicedetails
    - Remove field Visit_capacity from servicedetails
    - Create model ServiceDetails1
###



Migrations for 'store':
  store\migrations\0022_auto_20211024_1244.py
    - Create model ServiceDetailsDay
    - Rename field closing_time on shop to Closing_time
    - Rename field Integer_image on shop to Interior_image
    - Rename field offDay on shop to OffDay
    - Rename field opening_time on shop to Opening_time
    - Rename field shop_owner on shop to Shop_owner
    - Rename field shop_url on shop to Shop_url
    - Rename model ServiceDetails1 to ServiceDetailsDayTime
    - Delete model ServiceDetails
    - Add field ServiceDetailsDayID to servicedetailsdaytime
    - Alter unique_together for servicedetailsdaytime (1 constraint(s))
    - Remove field ServiceDetailsID from servicedetailsdaytime

***////
'''
