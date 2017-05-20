# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-20 10:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20170516_1156'),
        ('talks', '0011_auto_20170519_0944'),
    ]

    operations = [
        migrations.AddField(
            model_name='talk',
            name='event',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.PROTECT, related_name='talks', to='events.Event'),
            preserve_default=False,
        ),
    ]
