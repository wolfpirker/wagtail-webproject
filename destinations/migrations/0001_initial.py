# Generated by Django 2.2.4 on 2019-10-04 21:10

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tours', '0008_auto_20191004_2053'),
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('wagtailimages', '0001_squashed_0021'),
    ]

    operations = [
        migrations.CreateModel(
            name='DestinationPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('destination_name', models.CharField(help_text='enter the full location name', max_length=127)),
                ('body', wagtail.core.fields.RichTextField(blank=True)),
                ('lat_long', models.CharField(help_text="Comma separated lat/long. (Ex. 64.144367, -21.939182)                    Right click Google Maps and select 'What's Here'", max_length=36, validators=[django.core.validators.RegexValidator(code='invalid_lat_long', message='Lat Long must be a comma-separated numeric lat and long', regex='^(\\-?\\d+(\\.\\d+)?),\\s*(\\-?\\d+(\\.\\d+)?)$')])),
                ('province', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='tours.TourProvince')),
            ],
            options={
                'verbose_name_plural': 'Destination Pages',
                'verbose_name': 'Destination Page',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='DestinationsIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('intro', wagtail.core.fields.RichTextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Destination Index Pages',
                'verbose_name': 'Destination Index Page',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='DestinationPageCarouselImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('carousel_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='carousel_images', to='destinations.DestinationPage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
