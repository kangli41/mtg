# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-11-14 03:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0011_auto_20171114_1110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cardprice',
            name='card_id',
        ),
    ]
