# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-24 06:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talks', '0012_talk_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='talk',
            name='starts_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
