# Generated by Django 3.2.5 on 2022-05-01 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0023_alter_user_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='otp',
            field=models.IntegerField(default=4039),
        ),
    ]
