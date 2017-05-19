# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-04 19:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_groups'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReplacementDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, editable=False, max_length=254, verbose_name='название')),
                ('imei', models.CharField(blank=True, max_length=30, verbose_name='IMEI/SN')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Brand', verbose_name='бренд')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Model', verbose_name='модель')),
            ],
            options={
                'verbose_name_plural': 'устройства на замену',
                'verbose_name': 'устройство на замену',
                'ordering': ['-name'],
            },
        ),
        migrations.AddField(
            model_name='booking',
            name='replacement_device',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookings', to='crm.ReplacementDevice', verbose_name='устройство на замену'),
        ),
    ]