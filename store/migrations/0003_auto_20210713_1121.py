# Generated by Django 3.2.5 on 2021-07-13 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_service_servicedetails'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='opening_hours',
        ),
        migrations.AddField(
            model_name='shop',
            name='closing_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='shop',
            name='opening_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]