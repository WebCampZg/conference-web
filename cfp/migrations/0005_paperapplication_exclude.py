# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0004_auto_20150531_2008'),
    ]

    operations = [
        migrations.AddField(
            model_name='paperapplication',
            name='exclude',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
