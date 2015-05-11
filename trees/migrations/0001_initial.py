# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NotableTree',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city_object_id', models.FloatField(null=True)),
                ('city_tree_id', models.IntegerField(null=True)),
                ('city_status', models.CharField(default=b'None', max_length=20)),
                ('scientific_name', models.CharField(max_length=100)),
                ('common_name', models.CharField(max_length=100)),
                ('state_id', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=100)),
                ('height', models.IntegerField(null=True, blank=True)),
                ('spread', models.IntegerField(null=True, blank=True)),
                ('circumference', models.FloatField(null=True, blank=True)),
                ('diameter', models.FloatField(null=True, blank=True)),
                ('year_designated', models.IntegerField(null=True, blank=True)),
                ('owner', models.CharField(max_length=255, blank=True)),
                ('city_notes', models.TextField(blank=True)),
                ('latitude', models.DecimalField(max_digits=9, decimal_places=6, blank=True)),
                ('longitude', models.DecimalField(max_digits=9, decimal_places=6, blank=True)),
                ('designation', models.CharField(default=b'u', max_length=1, choices=[(b'h', b'Heritage Tree'), (b'm', b'Tree of Merit'), (b's', b'Significant'), (b'u', b'Undefined')])),
                ('initial_datasource', models.CharField(default=b'u', max_length=1, choices=[(b'c', b'City of Portland'), (b's', b'State of Oregon'), (b'e', b'Elsewise'), (b'f', b'Fan'), (b'u', b'Undefined or Other')])),
                ('display_icon', models.CharField(default=b'z', max_length=1, choices=[(b'h', b'Heritage Tree Icon'), (b'g', b'Ghost Tree Icon'), (b'n', b'No Access Icon'), (b'z', b'Other Tree Icon')])),
                ('deceased', models.BooleanField(default=False)),
                ('year_deceased', models.IntegerField(null=True, blank=True)),
                ('cause_of_death', models.CharField(max_length=255, blank=True)),
                ('internal_notes', models.TextField(blank=True)),
                ('legacy_uuid', models.CharField(max_length=64, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('mod_date', models.DateTimeField(auto_now=True, verbose_name=b'last modified')),
            ],
            options={
                'ordering': ['city_tree_id'],
            },
        ),
        migrations.CreateModel(
            name='TreeGenus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('genus_name', models.CharField(max_length=100)),
                ('common_name', models.CharField(max_length=100, blank=True)),
                ('slug', models.SlugField(unique=True)),
                ('notes', models.TextField(blank=True)),
                ('display_in_menu', models.BooleanField(default=False)),
                ('display_order', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['genus_name'],
                'verbose_name_plural': 'Genera',
            },
        ),
        migrations.AddField(
            model_name='notabletree',
            name='genus',
            field=models.ForeignKey(related_query_name=b'tree', related_name='trees', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='trees.TreeGenus', null=True),
        ),
    ]
