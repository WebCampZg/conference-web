# -*- coding: utf-8 -*-


from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0004_paperapplication_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='user',
            field=models.OneToOneField(related_name='applicant', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paperapplication',
            name='applicant',
            field=models.ForeignKey(related_name='applications', to='cfp.Applicant'),
            preserve_default=True,
        ),
    ]
