# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsors', '0004_auto_20150512_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='image',
            field=models.FileField(max_length=255, null=True, upload_to=b'uploads/sponsors/', blank=True),
            preserve_default=True,
        ),
    ]
