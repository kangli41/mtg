# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-11-14 03:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0009_auto_20171114_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardprice',
            name='card_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trade.CardInfo'),
        ),
    ]
