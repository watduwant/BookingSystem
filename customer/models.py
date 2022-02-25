from django.db import models
from auth_app.models import User
# from auth_app.models import Profile
from django.db.models.signals import post_save, post_delete
from store.models import ServiceDetailsDayTime

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


class Appointment(models.Model):
    Customer = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='customer')
    Service = models.ForeignKey(ServiceDetailsDayTime, on_delete=models.CASCADE, verbose_name='service', blank=True, null=True)
    PatientName  = models.CharField(max_length=200, verbose_name='patient_name')
    Age = models.IntegerField(null=False, blank=False, verbose_name='age')
    Sex = models.CharField(max_length=10, choices=Gender_Choices, verbose_name='gender')
    phone = models.CharField(max_length=10)
    Status = models.CharField(max_length=10, choices=Status_Choices, verbose_name='status', default='P')
    Rank  = models.IntegerField(default=0 , verbose_name='rank')

    day = models.CharField(max_length=50)
    time  = models.CharField(max_length=10, default="Noon")

    def __str__(self):
        return self.Customer.email + "--" + str(self.Service.Time) 

    def rank_generated(sender,instance, *args, **kwargs):
        appointment = instance
        service = appointment.Service
        day = appointment.day
        time = appointment.time
        rank_alloted = Appointment.objects.filter(Status="P", Service=service, day=day, time=time).count() + Appointment.objects.filter(Status="A", Service=service, day=day, time=time).count()
        print(rank_alloted)
        Appointment.objects.filter(id=appointment.id).update(Rank = rank_alloted)
    
    class Meta:
        ordering = ['day']

post_save.connect(Appointment.rank_generated, sender=Appointment)

