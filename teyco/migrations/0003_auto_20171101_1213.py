# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-01 12:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teyco', '0002_auto_20171101_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mandat',
            name='etatMandat',
            field=models.SmallIntegerField(),
        ),
    ]
