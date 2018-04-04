# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TShirtSize',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ['pk'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='user',
            name='github',
            field=models.CharField(max_length=39, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='tshirt_size',
            field=models.ForeignKey(blank=True, to='people.TShirtSize', on_delete=models.CASCADE, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='twitter',
            field=models.CharField(max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
    ]
