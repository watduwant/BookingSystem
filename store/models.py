from django.db import models

# Create your models here.
class Shop(models.Model):
    Name          = models.CharField(max_length=190, unique=True)
    Address       = models.CharField(max_length=300)
    Status        = models.IntegerField()
    Image         = models.ImageField(upload_to='shops', blank=True, null=True)
    opening_time  = models.TimeField(null=True, blank=True)
    closing_time  = models.TimeField(null=True, blank=True)

class Doctor(models.Model):
    Name           = models.CharField(max_length=100, unique=True)
    Specialization = models.CharField(max_length=200, blank=False)
    Image          = models.ImageField(upload_to='doctors', blank=True, null=True)


class Service(models.Model):

    Clinic = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True, blank=True)
    Doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    Date = models.DateField()


class ServiceDetails(models.Model):
    DayChoices = (
        ('S', 'SUNDAY'),
        ('M', 'MONDAY'),
        ('T', 'TUESDAY'),
        ('W', 'WEDNESDAY'),
        ('TH', 'THURSDAY'),
        ('F', 'FRIDAY'),
        ('ST', 'SATURDAY')
    )
    ServiceID = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    Time = models.TimeField()
    Fees = models.IntegerField()
    day = models.CharField(max_length=2, choices=DayChoices, null=True)
    Visit_capacity = models.IntegerField()