# -*- coding: utf-8 -*-


from django.db import models, migrations
import tinymce.models
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField()),
                ('name', models.CharField(unique=True, max_length=255)),
                ('type', models.CharField(default=b'standard', max_length=255, choices=[(b'diamond', b'Diamond'), (b'track', b'Track'), (b'standard', b'Standard'), (b'supporter', b'Supporter')])),
                ('about', tinymce.models.HTMLField()),
                ('url', models.URLField(max_length=255)),
                ('image', filebrowser.fields.FileBrowseField(max_length=255, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
