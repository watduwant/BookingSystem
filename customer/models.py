from django.db import models
# from auth_app.models import Profile
from django_lifecycle import LifecycleModel, hook, AFTER_SAVE, AFTER_UPDATE

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
    Rank = models.IntegerField(default=0, null=True, blank=True)
    slot_date = models.DateField(null=True, blank=True)
    time = models.TimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        # return self.appointment_user.email + "--" + str(self.Service.Time)
        return f"{self.id} - {self.Rank} "

    @hook(AFTER_SAVE, when='Status', was=APPOINTMENT_STATUS.PENDING)
    @hook(AFTER_UPDATE, when='Status', was=APPOINTMENT_STATUS.PENDING, is_now=APPOINTMENT_STATUS.ACCEPTED)
    @hook(AFTER_UPDATE, when='Status', was=APPOINTMENT_STATUS.ACCEPTED, is_now=APPOINTMENT_STATUS.CANCELLED)
    def rank_generated(self):
        rank_alloted = None
        if self.Status == APPOINTMENT_STATUS.PENDING:
            rank_alloted = Appointment.objects.filter(
                Status=APPOINTMENT_STATUS.PENDING,
                Service=self.Service,
                slot_date=self.slot_date
            ).count()
        elif self.Status == APPOINTMENT_STATUS.ACCEPTED:
            rank_alloted = Appointment.objects.filter(
                Status=APPOINTMENT_STATUS.ACCEPTED,
                Service=self.Service,
                slot_date=self.slot_date
            ).count()
        if rank_alloted == 0:
            rank_alloted += 1
        else:
            Appointment.objects.filter(
                id=self.id
            ).update(
                Rank=rank_alloted,
                time=self.time
            )
        if self.Status == APPOINTMENT_STATUS.CANCELLED:
            data = Appointment.objects.exclude(Status=APPOINTMENT_STATUS.CANCELLED).order_by('Rank')
            Appointment.objects.filter(id=self.id).update(Rank=0)

            new_ranks = []
            for index, obj in enumerate(data, start=1):
                obj.Rank = index
                new_ranks.append(obj)

            Appointment.objects.bulk_update(new_ranks, ['Rank'])
