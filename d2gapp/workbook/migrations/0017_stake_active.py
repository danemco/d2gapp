# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-20 01:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workbook', '0016_auto_20161103_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='stake',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
