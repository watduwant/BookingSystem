from django.db import models

# Create your models here.
class Shop(models.Model):
    Name          = models.CharField(max_length=190, unique=True)
    Address       = models.CharField(max_length=300)
    Status        = models.IntegerField()
    Image         = models.ImageField(upload_to='shops', blank=True, null=True)
    opening_hours = models.CharField(max_length=100)

class Doctor(models.Model):
    Name           = models.CharField(max_length=100, unique=True)
    Specialization = models.CharField(max_length=200, blank=False)
    Image          = models.ImageField(upload_to='doctors', blank=True, null=True)
    