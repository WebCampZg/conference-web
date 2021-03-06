# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-28 17:08


from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('voting', '0002_auto_20150813_2010'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoteToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_code', models.CharField(max_length=255)),
                ('token_sent', models.DateTimeField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
