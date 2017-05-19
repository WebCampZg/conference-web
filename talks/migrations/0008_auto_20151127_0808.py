# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talks', '0007_talk_slides_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='talk',
            name='video',
        ),
        migrations.AddField(
            model_name='talk',
            name='youtube_id',
            field=models.CharField(max_length=20, blank=True),
            preserve_default=True,
        ),
    ]
