# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-21 05:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workbook', '0010_auto_20160813_2332'),
    ]

    operations = [
        migrations.AddField(
            model_name='personprogress',
            name='reviewed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviewed_list', to='workbook.Profile'),
        ),
        migrations.AlterField(
            model_name='personprogress',
            name='shared_with',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='workbook.ProfileNotify'),
        ),
    ]
