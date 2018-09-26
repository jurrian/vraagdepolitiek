from django.db import migrations


def create_moderators_group(apps, schema_editor):
    """Give all permissions on Question except delete."""
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    add_question = Permission.objects.get(codename='add_question')
    view_question = Permission.objects.get(codename='view_question')
    change_question = Permission.objects.get(codename='change_question')
    publish_question = Permission.objects.get(codename='publish_question')

    group = Group.objects.create(pk=1, name='Moderators')
    group.permissions.add(add_question, view_question, change_question,
                          publish_question)
    group.save()


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_question_published'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'permissions': (('publish_question', 'Can publish question'),)},
        ),
        migrations.RunPython(create_moderators_group),
    ]
