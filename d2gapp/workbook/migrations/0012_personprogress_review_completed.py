# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-21 07:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workbook', '0011_auto_20160820_2350'),
    ]

    operations = [
        migrations.AddField(
            model_name='personprogress',
            name='review_completed',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
