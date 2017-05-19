# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talks', '0008_auto_20151127_0808'),
    ]

    operations = [
        migrations.AddField(
            model_name='talk',
            name='rate_url',
            field=models.URLField(blank=True),
            preserve_default=True,
        ),
    ]
