# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0006_auto_20150320_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='callforpaper',
            name='announcement',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
