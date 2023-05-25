from django.db import models
# from auth_app.models import Profile
from django_lifecycle import LifecycleModel, hook, AFTER_UPDATE

from api.static_variables import APPOINTMENT_STATUS
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
        verbose_name='who create the appointment'
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
    Status = models.CharField(
        max_length=10, choices=APPOINTMENT_STATUS.Status_Choices, verbose_name='status',
        default=APPOINTMENT_STATUS.PENDING
    )
    Rank = models.IntegerField(default=0, verbose_name='rank')
    date = models.DateField(null=True, blank=True)
    day = models.CharField(max_length=50)
    time = models.TimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.appointment_user.email + "--" + str(self.Service.Time)

    class Meta:
        ordering = ['day']

    @hook(AFTER_UPDATE, when='Status', was=APPOINTMENT_STATUS.PENDING, is_now=APPOINTMENT_STATUS.ACCEPTED)
    @hook(AFTER_UPDATE, when='Status', was=APPOINTMENT_STATUS.CANCELLED, is_now=APPOINTMENT_STATUS.ACCEPTED)
    def rank_generated(self):
        rank_alloted = Appointment.objects.filter(
            Status=APPOINTMENT_STATUS.ACCEPTED,
            Service=self.Service,
            day=self.day
        ).count()
        print(rank_alloted)
        if rank_alloted == 0:
            rank_alloted += 1
        else:
            Appointment.objects.filter(id=self.id).update(Rank=rank_alloted, time=self.time)