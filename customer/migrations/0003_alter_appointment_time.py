# Generated by Django 3.2.5 on 2023-05-11 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20230511_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='time',
            field=models.TimeField(auto_now_add=True, null=True),
        ),
    ]
