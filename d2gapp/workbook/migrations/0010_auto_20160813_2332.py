# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-14 05:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workbook', '0009_auto_20160727_2247'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='personprogress',
            options={'ordering': ['date_completed'], 'verbose_name_plural': 'person progress records'},
        ),
        migrations.AlterModelOptions(
            name='profilenotify',
            options={'verbose_name': 'profile notification', 'verbose_name_plural': 'profile notifications'},
        ),
        migrations.AddField(
            model_name='assignment',
            name='review',
            field=models.BooleanField(default=False, verbose_name='is this assignment a review item'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='office',
            field=models.CharField(choices=[('d', 'Deacon'), ('t', 'Teacher'), ('z', 'Priest'), ('-', 'Advisor, Bishop, or Parent')], default='d', max_length=2, verbose_name='priesthood office'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='section',
            field=models.CharField(choices=[('ss', 'Spiritual Strength'), ('pd', 'Priesthood Duties'), ('ftsoy', 'For The Strength Of Youth'), ('mp', 'Preparing To Receive the Melchizedek Priesthood')], default='ss', max_length=5),
        ),
        migrations.AlterField(
            model_name='profile',
            name='office',
            field=models.CharField(choices=[('d', 'Deacon'), ('t', 'Teacher'), ('z', 'Priest'), ('-', 'Advisor, Bishop, or Parent')], max_length=2, verbose_name='priesthood office'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, help_text='Use your full 10 digit phone number for receiving text messages', max_length=10, null=True, verbose_name='phone number'),
        ),
    ]
