# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-25 22:40
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('flatmates', '0007_auto_20160726_0404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenses',
            name='spent_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 25, 22, 40, 37, 299649, tzinfo=utc)),
        ),
    ]
