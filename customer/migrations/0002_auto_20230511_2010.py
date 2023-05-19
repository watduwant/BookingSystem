# Generated by Django 3.2.5 on 2023-05-11 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appointment',
            options={},
        ),
        migrations.AlterField(
            model_name='appointment',
            name='Status',
            field=models.CharField(choices=[('P', 'Pending'), ('A', 'Accepted'), ('C', 'Cancelled')], default='P', max_length=10, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]