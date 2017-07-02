# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-27 18:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsors', '0009_auto_20170519_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='type',
            field=models.CharField(choices=[(b'diamond', b'Diamond Sponsor'), (b'lanyard', b'Lanyard Sponsor'), (b'track', b'Track Sponsor'), (b'foodanddrinks', b'Food & Drinks Sponsor'), (b'standard', b'Standard Sponsor'), (b'supporter', b'Supporter Sponsor'), (b'mainmedia', b'Main Media Sponsor'), (b'media', b'Media sponsors')], default=b'standard', max_length=255),
        ),
    ]