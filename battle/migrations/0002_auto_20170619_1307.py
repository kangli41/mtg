# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-19 05:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='constructleague',
            old_name='during123',
            new_name='during',
        ),
    ]