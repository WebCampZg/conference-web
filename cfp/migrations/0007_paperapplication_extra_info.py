# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0006_paperapplication_accomodation_required'),
    ]

    operations = [
        migrations.AddField(
            model_name='paperapplication',
            name='extra_info',
            field=models.TextField(help_text=b'Anything else that you would like to let us know?', null=True, verbose_name=b'Extra info', blank=True),
            preserve_default=True,
        ),
    ]
