# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-28 04:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workbook', '0008_auto_20160722_2153'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assignment',
            options={'ordering': ['office', 'ordering']},
        ),
        migrations.AddField(
            model_name='assignment',
            name='act3',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='personprogress',
            name='act3',
            field=models.TextField(blank=True, null=True),
        ),
    ]
