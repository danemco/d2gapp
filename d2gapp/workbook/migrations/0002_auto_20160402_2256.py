# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-03 04:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workbook', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='section',
            field=models.CharField(choices=[('ss', 'Spiritual Strength'), ('pd', 'Priesthood Duties'), ('ftsoy', 'For The Strenght Of Youth'), ('mp', 'Preparing To Receive the Melchizedek Priesthood')], max_length=5),
        ),
    ]