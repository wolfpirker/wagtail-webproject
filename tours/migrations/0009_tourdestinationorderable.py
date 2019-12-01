# Generated by Django 2.2.4 on 2019-10-12 18:51

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('destinations', '0004_auto_20191012_1043'),
        ('tours', '0008_auto_20191004_2053'),
    ]

    operations = [
        migrations.CreateModel(
            name='TourDestinationOrderable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('destination_pages', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='destinations.DestinationPage')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tour_destinations', to='tours.TourPage')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
        ),
    ]