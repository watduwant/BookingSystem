# Generated by Django 3.2.5 on 2022-01-04 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='Status',
            field=models.CharField(choices=[('P', 'Pending'), ('A', 'Accepted'), ('C', 'Cancelled')], default='P', max_length=10, verbose_name='status'),
        ),
    ]
