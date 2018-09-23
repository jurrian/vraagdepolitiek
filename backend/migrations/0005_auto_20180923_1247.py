# Generated by Django 2.1.1 on 2018-09-23 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('backend', '0004_create_sites'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='organization',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='backend.Organization'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='efforts',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='pledges',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='site',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, to='sites.Site'),
        ),
        migrations.AddField(
            model_name='question',
            name='requests',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.Representative'),
        ),
        migrations.AlterField(
            model_name='question',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.Representative'),
        ),
    ]
