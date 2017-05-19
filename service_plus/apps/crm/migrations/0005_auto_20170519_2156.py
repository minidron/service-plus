# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-19 18:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_auto_20170517_2110'),
    ]

    operations = [
        migrations.AddField(
            model_name='sparepart',
            name='guarantees',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='spare_parts', to='crm.Guarantee', verbose_name='гарантия'),
        ),
        migrations.AddField(
            model_name='sparepartcount',
            name='guarantees',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='spare_part_counts', to='crm.Guarantee', verbose_name='гарантия'),
        ),
    ]
