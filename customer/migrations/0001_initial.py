# Generated by Django 3.2.5 on 2021-07-11 05:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Service', models.CharField(max_length=300, verbose_name='service')),
                ('PatientName', models.CharField(max_length=200, verbose_name='patient_name')),
                ('Age', models.IntegerField(max_length=2, verbose_name='age')),
                ('Sex', models.CharField(choices=[('Male', 'M'), ('Female', 'F'), ('Other', 'O')], max_length=10, verbose_name='gender')),
                ('Status', models.BooleanField(default=False, verbose_name='appointment_status')),
                ('Rank', models.IntegerField(max_length=2, verbose_name='rank')),
                ('Customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='customer')),
            ],
        ),
    ]