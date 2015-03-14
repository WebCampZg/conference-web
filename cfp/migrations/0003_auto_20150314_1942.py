# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0002_auto_20150301_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callforpaper',
            name='description',
            field=tinymce.models.HTMLField(),
            preserve_default=True,
        ),
    ]
