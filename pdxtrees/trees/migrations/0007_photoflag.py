# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trees', '0006_auto_20150508_1754'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhotoFlag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('flag_type', models.IntegerField(default=0, choices=[(0, b'Other'), (1, b'Incorrect Tree'), (2, b'Incorrect Comment')])),
                ('complaint', models.TextField()),
                ('flag_date', models.DateTimeField(auto_now_add=True)),
                ('reviewed', models.BooleanField(default=False)),
                ('review_date', models.DateTimeField(null=True, blank=True)),
                ('review_action', models.CharField(default=b'p', max_length=1, choices=[(b'p', b'Pending'), (b'c', b'Confirmed'), (b'r', b'Rejected')])),
                ('review_notes', models.TextField(blank=True)),
                ('flagged_photo', models.ForeignKey(related_query_name=b'flagged_photo', related_name='flagged_photos', on_delete=django.db.models.deletion.PROTECT, to='trees.TreePhoto')),
            ],
            options={
                'ordering': ['flag_date'],
                'verbose_name_plural': 'submitted Photo Flags',
            },
        ),
    ]
