# Generated by Django 3.2.5 on 2021-08-06 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_shop_shop_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='Date',
        ),
        migrations.RemoveField(
            model_name='servicedetails',
            name='day',
        ),
        migrations.AddField(
            model_name='service',
            name='day',
            field=models.CharField(choices=[('S', 'SUNDAY'), ('M', 'MONDAY'), ('T', 'TUESDAY'), ('W', 'WEDNESDAY'), ('TH', 'THURSDAY'), ('F', 'FRIDAY'), ('ST', 'SATURDAY')], max_length=2, null=True),
        ),
    ]