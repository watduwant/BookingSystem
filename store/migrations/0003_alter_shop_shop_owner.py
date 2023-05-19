# Generated by Django 3.2.5 on 2023-05-16 16:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0002_auto_20221120_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='Shop_owner',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shop_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
