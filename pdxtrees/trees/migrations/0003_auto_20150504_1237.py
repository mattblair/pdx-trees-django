# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trees', '0002_auto_20150504_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notabletree',
            name='unified_identifier',
            field=models.CharField(unique=True, max_length=10),
        ),
    ]
