# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-20 02:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workbook', '0017_stake_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
