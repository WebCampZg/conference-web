# Generated by Django 2.1.7 on 2019-04-02 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0023_auto_20190402_1041'),
        ('workshops', '0007_workshop_sold_out'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshop',
            name='application',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='workshop', to='cfp.PaperApplication'),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='starts_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
