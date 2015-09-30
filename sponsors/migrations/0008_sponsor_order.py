# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsors', '0007_remove_sponsor_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='order',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
