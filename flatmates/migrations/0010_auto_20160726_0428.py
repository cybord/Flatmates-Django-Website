# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-25 22:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flatmates', '0009_auto_20160726_0422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenses',
            name='spent_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
