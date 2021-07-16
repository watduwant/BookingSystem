from django.contrib import admin
from .models import HtmlVideo, CssVideo, PythonVideo, javascriptVideo, DjangoVideo, AngularVideo, DjangoProjectVideo, AngularProjectsVideo

# Register your models here.

admin.site.register((HtmlVideo, CssVideo, PythonVideo, javascriptVideo, DjangoVideo, AngularVideo, DjangoProjectVideo, AngularProjectsVideo))