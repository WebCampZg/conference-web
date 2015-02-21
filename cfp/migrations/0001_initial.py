# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('about', models.CharField(max_length=140)),
                ('biography', models.CharField(max_length=2048)),
                ('speaker_experience', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to=b'applicant_images')),
                ('twitter_handle', models.CharField(max_length=50)),
                ('github_username', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AudienceSkillLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CallForPaper',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=1024)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PaperApplication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('about', models.CharField(max_length=255)),
                ('abstract', models.CharField(max_length=1024)),
                ('applicant', models.ForeignKey(to='cfp.Applicant')),
                ('cfp', models.ForeignKey(to='cfp.CallForPaper')),
                ('skill_level', models.ForeignKey(to='cfp.AudienceSkillLevel')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TShirtSize',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='applicant',
            name='tshirt_size',
            field=models.ForeignKey(to='cfp.TShirtSize'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='applicant',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
