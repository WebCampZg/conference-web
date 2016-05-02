# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='title_in_hero',
            field=models.BooleanField(default=False, help_text=b'If enabled, the title will be displayed in the hero unit. Otherwise, it will be displayed in page body.', verbose_name=b'Title in hero unit'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='page',
            name='hero_type',
            field=models.CharField(default=b'main', help_text=b'Switches the header image.', max_length=20, choices=[(b'main', b'Main'), (b'blog', b'Blog'), (b'cfp', b'CFP')]),
            preserve_default=True,
        ),
    ]
