from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
statuses = (('cr', 'customer'), ('so', 'shopowner'))
class Profile(models.Model):
    user         = models.OneToOneField(User, on_delete=models.CASCADE)
    email        = models.EmailField()
    profile_pic  = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    phone        = models.CharField(max_length=15, blank=True)
    status       = models.CharField(max_length=20, null=True, choices=statuses, default=statuses[0][1])
    city         = models.CharField(max_length=50, blank=True)
    pincode      = models.CharField(max_length=8, blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()