from django.db import models


# Create your models here.
class MasterConfig(models.Model):
    appointment_slot_flexibility = models.IntegerField(default=30)

    def __str__(self):
        return f" appointment_slot_flexibility : {self.appointment_slot_flexibility}"
