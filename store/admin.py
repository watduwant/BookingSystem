from django.contrib import admin
from .models import Shop, Doctor, Service, ServiceDetails

# Register your models here.
admin.site.register(Shop)
admin.site.register(Doctor)
admin.site.register(Service)
admin.site.register(ServiceDetails)
