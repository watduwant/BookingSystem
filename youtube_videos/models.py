from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from fcm_django.models import FCMDevice

# Create your models here.

class HtmlVideo(models.Model):

    videoid = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    desc = models.TextField(default="")

    def __str__(self):
        return self.desc

@receiver(post_save, sender=HtmlVideo, dispatch_uid="knowledge_push_notification")
def post_save_youtube_video_receiver(sender, instance, *args, **kwargs):
    devices = FCMDevice.objects.all()
    devices.send_message(
        title="Django Tutorial New Html Video ({})".format(instance.title),
        body="{}".format(instance.desc),
        color="#ffa813",
        data={"type": "html video", "description": instance.desc}
    )


class CssVideo(models.Model):

    videoid = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    desc = models.TextField(default="")

    def __str__(self):
        return self.desc

@receiver(post_save, sender=CssVideo, dispatch_uid="knowledge_push_notification")
def post_save_youtube_video_receiver(sender, instance, *args, **kwargs):
    devices = FCMDevice.objects.all()
    devices.send_message(
        title="Django Tutorial New Css Video ({})".format(instance.title),
        body="{}".format(instance.desc),
        color="#ffa813",
        data={"type": "css video", "description": instance.desc}
    )

class PythonVideo(models.Model):

    videoid = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    desc = models.TextField(default="")

    def __str__(self):
        return self.desc

@receiver(post_save, sender=PythonVideo, dispatch_uid="knowledge_push_notification")
def post_save_youtube_video_receiver(sender, instance, *args, **kwargs):
    devices = FCMDevice.objects.all()
    devices.send_message(
        title="Django Tutorial New Python Video ({})".format(instance.title),
        body="{}".format(instance.desc),
        color="#ffa813",
        data={"type": "python video", "description": instance.desc}
    )

class javascriptVideo(models.Model):

    videoid = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    desc = models.TextField(default="")

    def __str__(self):
        return self.desc

@receiver(post_save, sender=javascriptVideo, dispatch_uid="knowledge_push_notification")
def post_save_youtube_video_receiver(sender, instance, *args, **kwargs):
    devices = FCMDevice.objects.all()
    devices.send_message(
        title="Django Tutorial New JavaScript Video ({})".format(instance.title),
        body="{}".format(instance.desc),
        color="#ffa813",
        data={"type": "javascript video", "description": instance.desc}
    )

class DjangoVideo(models.Model):

    videoid = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    desc = models.TextField(default="")

    def __str__(self):
        return self.desc

@receiver(post_save, sender=DjangoVideo, dispatch_uid="knowledge_push_notification")
def post_save_youtube_video_receiver(sender, instance, *args, **kwargs):
    devices = FCMDevice.objects.all()
    devices.send_message(
        title="Django Tutorial New Django Video ({})".format(instance.title),
        body="{}".format(instance.desc),
        color="#ffa813",
        data={"type": "django video", "description": instance.desc}
    )

class AngularVideo(models.Model):

    videoid = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    desc = models.TextField(default="")

    def __str__(self):
        return self.desc

@receiver(post_save, sender=AngularVideo, dispatch_uid="knowledge_push_notification")
def post_save_youtube_video_receiver(sender, instance, *args, **kwargs):
    devices = FCMDevice.objects.all()
    devices.send_message(
        title="Django Tutorial New Angular Video ({})".format(instance.title),
        body="{}".format(instance.desc),
        color="#ffa813",
        data={"type": "angular video", "description": instance.desc}
    )

class DjangoProjectVideo(models.Model):

    videoid = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    desc = models.TextField(default="")

    def __str__(self):
        return self.desc

@receiver(post_save, sender=DjangoProjectVideo, dispatch_uid="knowledge_push_notification")
def post_save_youtube_video_receiver(sender, instance, *args, **kwargs):
    devices = FCMDevice.objects.all()
    devices.send_message(
        title="Django Tutorial New Django Project Video ({})".format(instance.title),
        body="{}".format(instance.desc),
        color="#ffa813",
        data={"type": "django video", "description": instance.desc}
    )

class AngularProjectsVideo(models.Model):

    videoid = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    desc = models.TextField(default="")

    def __str__(self):
        return self.desc

@receiver(post_save, sender=AngularProjectsVideo, dispatch_uid="knowledge_push_notification")
def post_save_youtube_video_receiver(sender, instance, *args, **kwargs):
    devices = FCMDevice.objects.all()
    devices.send_message(
        title="Django Tutorial New Angular Project Video ({})".format(instance.title),
        body="{}".format(instance.desc),
        color="#ffa813",
        data={"type": "html video", "description": instance.desc}
    )
