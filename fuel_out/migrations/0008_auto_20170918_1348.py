# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-18 10:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fuel_out', '0007_auto_20170918_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fuelreports',
            name='fuel_data',
            field=models.DateTimeField(),
        ),
    ]
