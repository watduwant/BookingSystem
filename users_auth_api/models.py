from crum import get_current_user
from django.core import mail
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _
from multiselectfield import MultiSelectField

# Existing Code
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
import random


statuses = (('cr', 'customer'), ('so', 'shopowner'))
rand_otp = random.randint(1000, 9999)


class User(AbstractUser):
    username = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)

    # Existing Code 
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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = "App User"
        verbose_name_plural = "App Users"


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, related_name='profile')
    customer_id = models.CharField(max_length=10, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)


@receiver(post_save, sender=UserProfile, dispatch_uid="registration_notification")
def notify_new_user_registration(sender, created, instance, **kwargs):
    if created:
        try:
            subject = 'New user registration on app {}'.format("Starter Template")
            html_message = render_to_string(
                'admin-notifications/new-user-registration-notification.html',
                {
                    'email': instance.user.email,
                     'first_name': instance.user.first_name,
                     'last_name': instance.user.last_name,
                     'phone_number': instance.phone_number
                 }
            )
            plain_message = strip_tags(html_message)
            from_email = '{} <no-reply@appadminpanel.in>'.format("watduwant")
            to = 'sbairagi825@gmail.com'
            mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        except:
            pass








