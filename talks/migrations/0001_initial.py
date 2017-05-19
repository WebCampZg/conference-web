# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0004_auto_20150531_2008'),
    ]

    operations = [
        migrations.CreateModel(
            name='Talk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=255, blank=True)),
                ('about', models.TextField(blank=True)),
                ('abstract', models.TextField(blank=True)),
                ('duration', models.CharField(blank=True, max_length=255, null=True, choices=[(b'25', b'25 Minutes'), (b'45', b'45 Minutes')])),
                ('application', models.OneToOneField(to='cfp.PaperApplication')),
                ('skill_level', models.ForeignKey(blank=True, to='cfp.AudienceSkillLevel', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
