# Generated by Django 3.2.5 on 2021-10-13 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_alter_servicedetails_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='shop_url',
            field=models.URLField(default='www.watduwant.com'),
        ),
    ]
