# -*- coding: utf-8 -*-


from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsors', '0001_squashed_0012_auto_20170921_1332'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField()),
                ('title', models.CharField(max_length=255)),
                ('text', tinymce.models.HTMLField()),
                ('url', models.URLField(max_length=255)),
                ('sponsor', models.ForeignKey(to='sponsors.Sponsor', on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
