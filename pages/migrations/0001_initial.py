# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('flatpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='flatpages.FlatPage', on_delete=models.CASCADE)),
                ('meta_description', models.TextField(help_text=b'Used for og:description')),
                ('hero_type', models.CharField(default=b'main', max_length=20, choices=[(b'main', b'Main'), (b'blog', b'Blog'), (b'cfp', b'CFP')])),
            ],
            options={
            },
            bases=('flatpages.flatpage',),
        ),
    ]
