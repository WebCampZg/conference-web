# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cfp.models


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0005_auto_20150319_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='about',
            field=models.TextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='applicant',
            name='biography',
            field=models.TextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='applicant',
            name='image',
            field=models.ImageField(upload_to=cfp.models.get_applicant_avatar_path),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='applicant',
            name='speaker_experience',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='callforpaper',
            name='title',
            field=models.CharField(max_length=1024),
            preserve_default=True,
        ),
    ]
