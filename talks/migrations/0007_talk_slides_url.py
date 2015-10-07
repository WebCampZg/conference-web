# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talks', '0006_talk_co_presenter'),
    ]

    operations = [
        migrations.AddField(
            model_name='talk',
            name='slides_url',
            field=models.URLField(blank=True),
            preserve_default=True,
        ),
    ]
