# Generated by Django 2.1.1 on 2018-09-22 13:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='fb_support_count',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='twitter_support_count',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='user_support',
            field=models.ManyToManyField(blank=True, related_name='user_support', to=settings.AUTH_USER_MODEL),
        ),
    ]