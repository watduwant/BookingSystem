# Generated by Django 3.2.5 on 2023-05-16 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_auto_20230516_2252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='who_create',
        ),
    ]
