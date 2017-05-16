# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-31 17:23


from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usergroups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergroup',
            name='representatives',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
