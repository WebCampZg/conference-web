# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0003_auto_20150314_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='paperapplication',
            name='duration',
            field=models.CharField(default=b'25', help_text='What talk duration slot would you like?', max_length=255, verbose_name='Talk Duration Slot', choices=[(b'25', b'25 Minutes'), (b'45', b'45 Minutes')]),
            preserve_default=True,
        ),
    ]
