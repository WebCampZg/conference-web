# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0003_auto_20150521_0859'),
    ]

    operations = [
        migrations.AddField(
            model_name='paperapplication',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 31, 18, 8, 48, 125475, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paperapplication',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 31, 18, 8, 53, 786279, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
