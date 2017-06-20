# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-20 12:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0015_applicant_company_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='company_name',
            field=models.CharField(blank=True, help_text='Name of the company you work for. Optional.', max_length=100, verbose_name='Company name'),
        ),
        migrations.AlterField(
            model_name='paperapplication',
            name='accomodation_required',
            field=models.BooleanField(default=False, help_text='For people outside of the Zagreb area, we provide 3 nights in a hotel.', verbose_name='I require accomodation'),
        ),
    ]
