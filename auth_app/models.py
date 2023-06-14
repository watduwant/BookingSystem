import random  # from web

from django.contrib.auth.models import AbstractUser
from django.db import models
from django_lifecycle import hook, LifecycleModel, AFTER_CREATE

from api.static_variables import USER_STATUS
from .manager import UserManager

# # Create your models here.
rand_otp = random.randint(1000, 9999)  # from web


# class Profile(models.Model):
#     user         = models.OneToOneField(User, on_delete=models.CASCADE)
#     email        = models.EmailField()
#     profile_pic  = models.ImageField(upload_to='profile_pics', blank=True, null=True)
#     phone        = models.CharField(max_length=15, blank=True)
#     status       = models.CharField(max_length=20, null=True, choices=statuses, default=statuses[0][1])
#     city         = models.CharField(max_length=50, blank=True)
#     pincode      = models.CharField(max_length=8, blank=True)

#     def __str__(self):
#         return self.user.username

# @receiver(post_save, sender = User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


class User(AbstractUser, LifecycleModel):
    username = None
    email = models.EmailField(unique=True)
    is_PhoneVerified = models.BooleanField(default=False)  # from web
    is_EmailVerified = models.BooleanField(default=False)  # from web
    email_token = models.CharField(max_length=100, null=True, blank=True)
    forgot_password = models.CharField(max_length=100, null=True, blank=True)
    last_login_time = models.DateTimeField(null=True, blank=True)
    last_logout_time = models.DateTimeField(null=True, blank=True)
    objects = UserManager()

    # extra fields 
    mobile = models.CharField(max_length=15, blank=True, null=True)
    # otp = models.IntegerField(default=rand_otp)  # from web
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    status = models.CharField(max_length=20, choices=USER_STATUS.USER_ROLE)

    # billing address  #from web
    city = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=200, default="NULL")
    flat_name = models.CharField(max_length=200, default="NULL")
    landmark = models.CharField(max_length=200, default="NULL")
    pincode = models.CharField(max_length=8, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
