# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-03 21:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workbook', '0015_auto_20161029_2246'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stake',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='unit',
            name='stake',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='workbook.Stake'),
        ),
    ]
