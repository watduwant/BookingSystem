# Generated by Django 3.2.5 on 2021-08-14 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0012_merge_20210814_1720'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appointment',
            options={'ordering': ['date']},
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='Created',
        ),
    ]
