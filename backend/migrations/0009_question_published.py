# Generated by Django 2.1.1 on 2018-09-25 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_auto_20180925_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='published',
            field=models.BooleanField(default=False, help_text='If the question has been published on the site.'),
        ),
    ]