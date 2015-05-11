# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trees', '0003_auto_20150504_1237'),
    ]

    operations = [
        migrations.RenameField(
            model_name='treephoto',
            old_name='RelatedTree',
            new_name='related_tree',
        ),
        migrations.AlterField(
            model_name='notabletree',
            name='city_object_id',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='notabletree',
            name='city_tree_id',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
