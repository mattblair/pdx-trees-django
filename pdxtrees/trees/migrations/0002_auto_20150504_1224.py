# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trees', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TreePhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submitted_image', models.ImageField(null=True, upload_to=b'submitted_photos/%Y/%m/%d', blank=True)),
                ('submitted_tree_id', models.IntegerField(null=True, blank=True)),
                ('submitted_caption', models.TextField(blank=True)),
                ('submitted_name', models.CharField(max_length=100, blank=True)),
                ('submitted_email', models.CharField(max_length=200, blank=True)),
                ('submitted_url', models.CharField(max_length=200, blank=True)),
                ('submitted_date', models.DateTimeField()),
                ('submitted_user_agent', models.CharField(max_length=255, blank=True)),
                ('submitted_latitude', models.DecimalField(max_digits=9, decimal_places=6, blank=True)),
                ('submitted_longitude', models.DecimalField(max_digits=9, decimal_places=6, blank=True)),
                ('review_status', models.CharField(default=b'p', max_length=10, choices=[(b'p', b'Pending'), (b'a', b'Approved'), (b'r', b'Rejected'), (b't', b'Testing Only')])),
                ('review_notes', models.TextField(blank=True)),
                ('reviewed_date', models.DateTimeField()),
                ('approved_image_filename', models.CharField(max_length=150, blank=True)),
                ('approved_photograher_name', models.CharField(max_length=100, blank=True)),
                ('approved_caption', models.TextField(blank=True)),
                ('legacy_uuid', models.CharField(max_length=64, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('mod_date', models.DateTimeField(auto_now=True, verbose_name=b'last modified')),
            ],
            options={
                'ordering': ['created_date'],
            },
        ),
        migrations.AlterModelOptions(
            name='notabletree',
            options={'ordering': ['unified_identifier']},
        ),
        migrations.AddField(
            model_name='notabletree',
            name='unified_identifier',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='treephoto',
            name='RelatedTree',
            field=models.ForeignKey(related_query_name=b'photographed_tree', related_name='photographed_trees', on_delete=django.db.models.deletion.PROTECT, blank=True, to='trees.NotableTree', null=True),
        ),
    ]
