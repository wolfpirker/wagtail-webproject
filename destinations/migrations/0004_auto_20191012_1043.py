# Generated by Django 2.2.4 on 2019-10-12 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('destinations', '0003_auto_20191012_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destinationpage',
            name='use_destination_name_as_map_location',
            field=models.BooleanField(default=True, help_text='instead of coordinates use the location name for the map'),
        ),
    ]
