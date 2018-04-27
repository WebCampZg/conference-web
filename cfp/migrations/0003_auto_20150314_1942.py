# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callforpaper',
            name='description',
            field=models.TextField(),
            preserve_default=True,
        ),
    ]
