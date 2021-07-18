# Generated by Django 3.1.5 on 2021-07-15 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_auto_20210713_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='Status',
            field=models.CharField(blank=True, choices=[('P', 'Pending'), ('A', 'Accepted'), ('C', 'Cancelled')], max_length=10, null=True, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
