# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-11-14 02:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0005_cardinfo_cardprice'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardinfo',
            name='card_image_link',
            field=models.CharField(default='', max_length=200),
        ),
    ]
