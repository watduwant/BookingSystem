from django.db import models
from django.contrib.auth.models import User
# from auth_app.models import Profile
from django.db.models.signals import post_save, post_delete
from store.models import Service

# Create your models here.

Gender_Choices  = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)
Status_Choices  = (
    ('P', 'Pending'),
    ('A', 'Accepted'),
    ('C', 'Cancelled'),
)
# prof = Profile.objects.filter(status='customer')
# user = User.Profile.objects.filter(Profile=prof)
class Appointment(models.Model):
    Customer = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='customer')
    Service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='service', blank=True, null=True)
    PatientName  = models.CharField(max_length=200, verbose_name='patient_name')
    Age = models.IntegerField(null=False, blank=False, verbose_name='age')
    Sex = models.CharField(max_length=10, choices=Gender_Choices, verbose_name='gender')
    phone = models.CharField(max_length=10)
    Status = models.CharField(max_length=10, choices=Status_Choices, verbose_name='status', null=True, blank=True)
    Rank  = models.IntegerField(default=0 , verbose_name='rank')
    date  = models.DateField(null=True, blank=True)
    time  = models.CharField(max_length=10, default="Noon")

    def __str__(self):
        return self.Customer.username + "--" + self.Service.get_name 

    def rank_generated(instance, sender, *args, **kwargs):
        appointment = instance
        service = appointment.Service
        rank_alloted = Appointment.objects.filter(Status="P", Service=service).count() + Appointment.objects.filter(Status="A", Service=service).count()
        Appointment.objects.filter(id=appointment.id).update(Rank = rank_alloted)
    
    class Meta:
        ordering = ['date']

post_save.connect(Appointment.rank_generated, sender=Appointment)

