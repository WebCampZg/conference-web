# Generated by Django 2.1.8 on 2019-05-27 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
        ('cfp', '0024_auto_20190430_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='paperapplication',
            name='labels',
            field=models.ManyToManyField(related_name='applications', to='labels.Label'),
        ),
    ]
