# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-15 14:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fuel_out', '0005_auto_20170913_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fuelreports',
            name='fuel_data',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='fuelreports',
            name='fuel_number',
            field=models.IntegerField(default=0),
        ),
    ]