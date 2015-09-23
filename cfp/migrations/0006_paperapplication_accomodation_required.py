# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0005_paperapplication_exclude'),
    ]

    operations = [
        migrations.AddField(
            model_name='paperapplication',
            name='accomodation_required',
            field=models.BooleanField(default=False, help_text=b'For people outside of the Zagreb area, we provide 2 nights in a hotel.', verbose_name=b'I require accomodation'),
            preserve_default=True,
        ),
    ]
