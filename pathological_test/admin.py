from django.contrib import admin
from pathological_test.models import *


@admin.register(PathologicalTest)
class PathologicalTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'sample_type', 'description', 'precautions')
    search_fields = ('name', )


@admin.register(PathologicalTestDetail)
class PathologicalTestDetailAdmin(admin.ModelAdmin):
    list_display = (
        'clinic', 'test_name',
        'fees', 'delivery_duration'
        )
    list_filter = ('test_name', 'clinic')
    autocomplete_fields = ('test_name',)
    fields = (
        ('test_name', 'clinic'),
        ('image', ),
        ('delivery_duration', ),
        ('fees',)
    )

admin.site.register((ShopingCart, OrderDetail, UserOrder, Phlebotomist))