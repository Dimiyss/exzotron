# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-18 10:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fuel_out', '0006_auto_20170915_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fuelreports',
            name='fuel_data',
            field=models.DateField(),
        ),
    ]
