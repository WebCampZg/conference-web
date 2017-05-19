# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsors', '0003_sponsor_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='image',
            field=models.FileField(max_length=255, null=True, upload_to=b'uploads/', blank=True),
            preserve_default=True,
        ),
    ]
