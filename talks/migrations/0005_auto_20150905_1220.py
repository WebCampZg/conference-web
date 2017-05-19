# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talks', '0004_talk_keynote'),
    ]

    operations = [
        migrations.AddField(
            model_name='talk',
            name='is_community_chosen',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='talk',
            name='is_sponsored',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
