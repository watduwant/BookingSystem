from django.db import models
from users_auth_api.models import User
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
    time  = models.CharField(max_length=10, null=True, blank=True, default='Null')

    def __str__(self):
        return self.Customer.email + "--" + str(self.Service.Time) 

    def rank_generated(sender,instance, *args, **kwargs):
        service = instance.Service
        # day = service.ServiceDetailsDayID.Day
        time = service.Time
        rank_alloted = Appointment.objects.filter(Status="P", Service=service).count() + Appointment.objects.filter(Status="A", Service=service).count()
        print(rank_alloted+1)
        Appointment.objects.filter(id=instance.id).update(Rank = rank_alloted+1, time=time)
    
    class Meta:
        ordering = ['day']

post_save.connect(Appointment.rank_generated, sender=Appointment)

