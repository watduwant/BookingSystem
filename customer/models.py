import logging

from django.db import models
# from auth_app.models import Profile
from django_lifecycle import LifecycleModel, hook, AFTER_SAVE

from auth_app.models import User
from store.models import ServiceDetailsDayTime

# Create your models here.

Gender_Choices = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)
Status_Choices = (
    ('P', 'Pending'),
    ('A', 'Accepted'),
    ('C', 'Cancelled'),
)


# prof = Profile.objects.filter(status='customer')
# user = User.Profile.objects.filter(Profile=prof)
class Appointment(LifecycleModel):
    appointment_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='customer_appointment',
        verbose_name='patient_detail_code'
    )
    Service = models.ForeignKey(
        ServiceDetailsDayTime,
        on_delete=models.DO_NOTHING,
        verbose_name='service',
        blank=True,
        null=True
    )
    PatientName = models.CharField(max_length=200, verbose_name='patient_name')
    Age = models.IntegerField(null=False, blank=False, verbose_name='age')
    Sex = models.CharField(max_length=10, choices=Gender_Choices, verbose_name='gender')
    phone = models.CharField(max_length=10)
    Status = models.CharField(max_length=10, choices=Status_Choices, verbose_name='status', default='P')
    Rank = models.IntegerField(default=0, verbose_name='rank')
    date = models.DateField(null=True, blank=True)
    day = models.CharField(max_length=50)
    time = models.TimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.appointment_user.email + "--" + str(self.Service.Time)

    @hook(AFTER_SAVE)
    def rank_generated(self):
        service = self.Service
        day = self.day
        time = self.time
        rank_alloted = Appointment.objects.filter(
            Status="P",
            Service=service,
            day=day
        ).count() + Appointment.objects.filter(
            Status="A",
            Service=service,
            day=day
        ).count()
        logging.warning(f"rank is: {rank_alloted + 1}")
        Appointment.objects.filter(id=self.id).update(Rank=rank_alloted, time=time)

        class Meta:
            ordering = ['day']

#     def rank_generated(sender, instance, *args, **kwargs):
#         appointment = instance
#         service = appointment.Service
#         day = appointment.day
#         # day = service.ServiceDetailsDayID.Day
#         time = service.Time
#         rank_alloted = Appointment.objects.filter(
#             Status="P", Service=service,
#             day=day).count() + Appointment.objects.filter(
#             Status="A",
#             Service=service,
#             day=day
#         ).count()
#         print(rank_alloted + 1)
#         Appointment.objects.filter(id=instance.id).update(Rank=rank_alloted, time=time)
#
#     class Meta:
#         ordering = ['day']
#
#
# post_save.connect(Appointment.rank_generated, sender=Appointment)
