from django.db import migrations


def create_moderators_group(apps, schema_editor):
    """Give all permissions on Question except delete."""

    ContentType = apps.get_model('contenttypes', 'ContentType')
    Question = apps.get_model('backend', 'Question')

    content_type = ContentType.objects.get_for_model(Question)

    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    add_question = Permission.objects.get(codename='add_question')
    view_question = Permission.objects.get(codename='view_question')
    change_question = Permission.objects.get(codename='change_question')
    publish_question, _ = Permission.objects.get_or_create(
        codename='publish_question',
        name='Can publish question',
        content_type=content_type,
    )

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
