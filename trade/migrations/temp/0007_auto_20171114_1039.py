# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-11-14 02:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0006_cardinfo_card_image_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardprice',
            name='commander',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='cardprice',
            name='legacy',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='cardprice',
            name='modern',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='cardprice',
            name='standard',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='cardprice',
            name='vintage',
            field=models.IntegerField(default=0),
        ),
    ]
