# Generated by Django 2.2.4 on 2019-10-04 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0007_delete_tourcategoryindexpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tourpage',
            name='tour_duration',
            field=models.DurationField(blank=True, help_text="duration usual for this tour - type as 'DD HH:MM:SS' or 'HH:MM:SS'", null=True),
        ),
    ]
