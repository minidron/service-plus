# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-19 18:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_auto_20170519_2156'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sparepart',
            old_name='guarantees',
            new_name='guarantee',
        ),
        migrations.RenameField(
            model_name='sparepartcount',
            old_name='guarantees',
            new_name='guarantee',
        ),
    ]
