from __future__ import unicode_literals

from django.contrib.auth.management import create_permissions
from django.db import migrations


def create_group(apps, name, perms=[]):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    group, created = Group.objects.get_or_create(name=name)
    if created:
        for perm in perms:
            permission = Permission.objects.get(codename=perm)
            group.permissions.add(permission)


def apply_migration(apps, schema_editor):
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, apps=apps, verbosity=0)
        app_config.models_module = None
    create_group(apps, 'Приемщик', [])
    create_group(apps, 'Мастер', [
        'change_booking',
        'add_brand', 'change_brand', 'delete_brand',
        'add_model', 'change_model', 'delete_model',
    ])


def revert_migration(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=['Приемщик', 'Мастер']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(apply_migration, revert_migration)
    ]
