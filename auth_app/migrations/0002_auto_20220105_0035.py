# Generated by Django 3.2.5 on 2022-01-04 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_verified',
            new_name='is_EmailVerified',
        ),
        migrations.AddField(
            model_name='user',
            name='is_PhoneVerified',
            field=models.BooleanField(default=False),
        ),
    ]
