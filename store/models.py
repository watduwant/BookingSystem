from django.db import models
from django.contrib.auth.models import User
from auth_app.models import Profile

# Create your models here.
week_days = (
    ('6', 'Sunday'),
    ('0', 'Monday'),
    ('1', 'Tuesday'),
    ('2', 'Wednesday'),
    ('3', 'Thursday'),
    ('4', 'Friday'),
    ('5', 'Saturday'),
)
class Shop(models.Model):
    shop_status = (
        ('E', 'ENABLE'),
        ('D', 'DISABLE')
    )
    Name          = models.CharField(max_length=190, unique=True)
    shop_owner    = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    Address       = models.CharField(max_length=300)
    Status        = models.CharField(max_length=2, choices=shop_status, default='E')
    Integer_image = models.ImageField(upload_to='shops', blank=True, null=True)
    offDay        = models.CharField(max_length=5 ,default=1, choices=week_days)
    Image         = models.ImageField(upload_to='shops', blank=True, null=True)
    opening_time  = models.TimeField(null=True, blank=True)
    closing_time  = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.Name

class Doctor(models.Model):
    Name           = models.CharField(max_length=100, unique=True)
    Specialization = models.CharField(max_length=200, blank=False)
    Experience     = models.FloatField()
    Image          = models.ImageField(upload_to='doctors', blank=True, null=True)

    def __str__(self):
        return self.Name


class Service(models.Model):
    DayChoices = (
        ('S', 'SUNDAY'),
        ('M', 'MONDAY'),
        ('T', 'TUESDAY'),
        ('W', 'WEDNESDAY'),
        ('TH', 'THURSDAY'),
        ('F', 'FRIDAY'),
        ('ST', 'SATURDAY')
    )
    Clinic = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True, blank=True)
    day = models.CharField(max_length=2, choices=DayChoices, null=True)
    Doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def get_name(self):
        return self.Clinic.Name + "--" + self.Doctor.Name + "--" + self.day

    def __str__(self):
        return self.get_name



class ServiceDetails(models.Model):
    ServiceID = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    Time = models.TimeField()
    Fees = models.IntegerField()
    Visit_capacity = models.IntegerField() 

    def __str__(self):
        return self.ServiceID.get_name + "--" + str(self.Time)