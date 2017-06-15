# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-15 07:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cfp', '0014_auto_20170605_1545'),
        ('events', '0004_auto_20170516_1156'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='title', unique=True)),
                ('about', models.TextField()),
                ('abstract', models.TextField()),
                ('venue', models.TextField()),
                ('starts_at', models.DateTimeField()),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workshops', to='cfp.Applicant')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='workshops', to='events.Event')),
                ('skill_level', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cfp.AudienceSkillLevel')),
            ],
        ),
    ]
