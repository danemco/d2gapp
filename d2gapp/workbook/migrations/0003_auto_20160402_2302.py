# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-03 05:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workbook', '0002_auto_20160402_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='act2',
            field=models.TextField(blank=True, null=True),
        ),
    ]
