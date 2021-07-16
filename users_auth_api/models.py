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


class User(AbstractUser):
    username = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = "App User"
        verbose_name_plural = "App Users"


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, related_name='profile')
    customer_id = models.CharField(max_length=10, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    app_source = models.CharField(max_length=50, null=True, blank=True)
    django_tutorial_subscription = models.BooleanField(default=False, help_text="Check this field to remove Django Tutorial popup blocker for this user")
    angular_tutorial_subscription = models.BooleanField(default=False, help_text="Check this field to remove Angular Tutorial popup blocker for this user")
    angular_project_subscription = models.BooleanField(default=False, help_text="Check this field to remove Angular Tutorial popup blocker for this user")
    django_project_subscription = models.BooleanField(default=False, help_text="Check this field to remove Angular Tutorial popup blocker for this user")

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)


@receiver(post_save, sender=UserProfile, dispatch_uid="registration_notification")
def notify_new_user_registration(sender, created, instance, **kwargs):
    if created:
        try:
            subject = 'New user registration on app {}'.format(instance.app_source)
            html_message = render_to_string(
                'admin-notifications/new-user-registration-notification.html',
                {
                    'app_source': instance.app_source,
                    'email': instance.user.email,
                     'first_name': instance.user.first_name,
                     'last_name': instance.user.last_name,
                     'phone_number': instance.phone_number
                 }
            )
            plain_message = strip_tags(html_message)
            from_email = '{} <no-reply@appadminpanel.in>'.format(instance.app_source)
            if instance.app_source == "ifl_services":
                to = 'sbairagi825@gmail.com'
            elif instance.app_source == "EquityGlobal" :
                to = 'sbairagi825@gmail.com'
            else:
                to = 'sbairagi825@gmail.com'
            mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        except:
            pass







