# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsors', '0002_auto_20150510_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='is_active',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
