# Generated by Django 3.2.5 on 2022-05-03 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_auto_20220305_0033'),
        ('pathological_test', '0005_orderdetail_sample_collected_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='clinic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clinic_detail', to='store.shop'),
        ),
    ]
