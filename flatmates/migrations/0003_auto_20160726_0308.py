# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-25 21:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flatmates', '0002_expenses'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expenses',
            old_name='user_id',
            new_name='user_name',
        ),
    ]
