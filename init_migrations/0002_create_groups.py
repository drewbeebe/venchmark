from django.db import models, migrations


def apply_migration(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.bulk_create([
        Group(name=u'owner'),
        Group(name=u'vendor'),
        Group(name=u'analyst'),
        Group(name=u'auditor'),
    ])


def revert_migration(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(
        name__in=[
            u'owner',
            u'vendor',
            u'analyst',
            u'auditor',
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(apply_migration, revert_migration)
    ]
