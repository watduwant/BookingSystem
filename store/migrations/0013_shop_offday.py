# Generated by Django 3.2.5 on 2021-09-09 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_shop_integer_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='offDay',
            field=models.CharField(choices=[('1', 'Sunday'), ('2', 'Monday'), ('3', 'Tuesday'), ('4', 'Wednesday'), ('5', 'Thursday'), ('6', 'Friday'), ('7', 'Saturday')], default=1, max_length=5),
        ),
    ]
