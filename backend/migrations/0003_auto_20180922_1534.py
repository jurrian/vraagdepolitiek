# Generated by Django 2.1.1 on 2018-09-22 13:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20180922_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='user_support',
            field=models.ManyToManyField(blank=True, related_name='user_support_set', to=settings.AUTH_USER_MODEL),
        ),
    ]