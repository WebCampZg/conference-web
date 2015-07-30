# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talks', '0003_talk_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='talk',
            name='keynote',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
