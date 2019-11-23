# Generated by Django 2.2.4 on 2019-11-23 15:27

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('tours', '0009_tourdestinationorderable'),
        ('wagtailimages', '0001_squashed_0021'),
        ('ourteam', '0005_auto_20190911_1946'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ourteampage',
            options={'verbose_name': 'Our Team Page', 'verbose_name_plural': 'Our Team Pages'},
        ),
        migrations.CreateModel(
            name='TourGuide',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('body', wagtail.core.fields.RichTextField(blank=True)),
                ('include_contact_form', models.BooleanField()),
                ('contact_email', models.CharField(max_length=100)),
                ('allow_direct_guide_booking', models.BooleanField(help_text='wether this guide agrees to be booked for the hourly rate plus additional charge')),
                ('hourly_rate_low_season', models.IntegerField(help_text='hourly rate low season')),
                ('hourly_rate_high_season', models.IntegerField(help_text='hourly rate high season')),
                ('additional_charge_per_tour', models.IntegerField(help_text='added charge per group for each tour')),
                ('image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('main_province', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='tours.TourProvince')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='GuideToursOrderable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='guide_tours', to='tours.TourPage')),
                ('tours_pages', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='tours.TourPage')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
        ),
    ]
