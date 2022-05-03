# Generated by Django 3.2.5 on 2022-05-01 06:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pathological_test', '0003_phlebotomist'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_for', models.CharField(max_length=35)),
                ('pickup_date', models.DateField()),
                ('pickup_from', models.TextField()),
                ('zipcode', models.CharField(max_length=10)),
                ('contact', models.CharField(max_length=12)),
                ('status', models.CharField(choices=[('0', 'Not assigned'), ('1', 'Assigned'), ('2', 'delivered'), ('3', 'Not Delivered'), ('4', 'Collected'), ('5', 'Not Collected')], default='0', max_length=1)),
                ('transaction_id', models.CharField(blank=True, max_length=12, null=True)),
                ('total_price', models.FloatField(default=0)),
                ('date_of_order', models.DateField(auto_now=True)),
                ('complete', models.BooleanField(default=False)),
                ('payment_done', models.BooleanField(default=False)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_order', to='pathological_test.userorder')),
                ('phlebotomist', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pathological_test.phlebotomist')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='OrderAddresh',
        ),
    ]
