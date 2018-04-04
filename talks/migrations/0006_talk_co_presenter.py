# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0005_paperapplication_exclude'),
        ('talks', '0005_auto_20150905_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='talk',
            name='co_presenter',
            field=models.ForeignKey(related_name='co_talks', blank=True, to='cfp.Applicant', on_delete=models.CASCADE, null=True),
            preserve_default=True,
        ),
    ]
