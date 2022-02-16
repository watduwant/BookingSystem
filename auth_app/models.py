from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
import random


# # Create your models here.
statuses = (('cr', 'customer'), ('so', 'shopowner'))
rand_otp = random.randint(1000, 9999)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_PhoneVerified = models.BooleanField(default=False)
    is_EmailVerified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    forgot_password = models.CharField(max_length=100, null=True, blank=True)
    last_login_time = models.DateTimeField(null=True, blank=True)
    last_logout_time = models.DateTimeField(null=True, blank=True)
    objects = UserManager()

    # extra fields 
    mobile       = models.CharField(max_length=15, blank=True, null=True)
    otp          = models.IntegerField(default=rand_otp)
    profile_pic  = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    status       = models.CharField(max_length=20, null=True, choices=statuses, default=statuses[0][1])

    # billing address 
    city         = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=200, default="NULL")
    flat_name = models.CharField(max_length=200, default="NULL")
    landmark = models.CharField(max_length=200, default="NULL")
    pincode      = models.CharField(max_length=8, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []



