# Generated by Django 3.2.5 on 2021-09-17 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0014_alter_appointment_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='time',
            field=models.CharField(default='Noon', max_length=10),
        ),
    ]
