# Generated by Django 3.2.5 on 2022-02-11 11:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0012_order_paymentdone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='Clinic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='services', to='store.shop'),
        ),
        migrations.AlterField(
            model_name='service',
            name='Doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='services', to='store.doctor'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='Shop_owner',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]