# -*- coding: utf-8 -*-


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
                ('speaker_experience', models.CharField(max_length=255, null=True, blank=True)),
                ('image', models.ImageField(upload_to=b'applicant_images')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
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
                'ordering': ['pk'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CallForPaper',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=1024)),
                ('begin_date', models.DateField()),
                ('end_date', models.DateField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PaperApplication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text='The title of your talk. Keep it short and catchy.', max_length=255, verbose_name='Title')),
                ('about', models.TextField(help_text='Describe your talk in 140 characters or less.', verbose_name="What's it about")),
                ('abstract', models.TextField(help_text='You may go in more depth here. Up to 10 sentnces, please.', verbose_name='Abstract')),
                ('applicant', models.ForeignKey(to='cfp.Applicant', on_delete=models.CASCADE)),
                ('cfp', models.ForeignKey(to='cfp.CallForPaper', on_delete=models.CASCADE)),
                ('skill_level', models.ForeignKey(verbose_name='Audience level', to='cfp.AudienceSkillLevel', on_delete=models.CASCADE, help_text='Which skill level is this talk most appropriate for?')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
