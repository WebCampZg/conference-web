# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='application',
            field=models.ForeignKey(related_name='votes', to='cfp.PaperApplication'),
            preserve_default=True,
        ),
    ]
