# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsors', '0005_auto_20150521_0859'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='location',
            field=models.CharField(default=b'Zagreb, Croatia', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='type',
            field=models.CharField(default=b'standard', max_length=255, choices=[(b'diamond', b'Diamond Sponsor'), (b'track', b'Track Sponsor'), (b'foodanddrinks', b'Food & Drinks Sponsor'), (b'standard', b'Standard Sponsor'), (b'supporter', b'Supporter Sponsor'), (b'mainmedia', b'Main Media Sponsor'), (b'media', b'Media sponsors')]),
            preserve_default=True,
        ),
    ]
