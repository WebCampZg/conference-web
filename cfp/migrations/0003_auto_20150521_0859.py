# -*- coding: utf-8 -*-


from django.db import models, migrations
import cfp.models


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0002_auto_20150301_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='image',
            field=models.ImageField(max_length=255, upload_to=cfp.models.get_applicant_avatar_path),
            preserve_default=True,
        ),
    ]
