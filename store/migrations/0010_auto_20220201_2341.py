# Generated by Django 3.2.5 on 2022-02-01 18:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0009_alter_order_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='age',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='patientName',
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='User',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shippingAddress', to=settings.AUTH_USER_MODEL),
        ),
    ]
