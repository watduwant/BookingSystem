# Generated by Django 3.2.5 on 2021-08-02 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0007_profile_profile_pic'),
        ('store', '0008_auto_20210803_0032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='shop_owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth_app.profile'),
        ),
    ]
