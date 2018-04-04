# -*- coding: utf-8 -*-


from django.db import models, migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('talks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='talk',
            name='video',
            field=filebrowser.fields.FileBrowseField(max_length=255, null=True, verbose_name=b'Video', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='talk',
            name='application',
            field=models.OneToOneField(related_name='talk', to='cfp.PaperApplication', on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
