# Generated by Django 3.2.5 on 2021-08-02 19:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0007_auto_20210723_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='shop_owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='shop',
            name='Status',
            field=models.CharField(choices=[('E', 'ENABLE'), ('D', 'DISABLE')], default='E', max_length=2),
        ),
    ]
