# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trees', '0004_auto_20150505_1204'),
    ]

    operations = [
        migrations.RenameField(
            model_name='treephoto',
            old_name='approved_photograher_name',
            new_name='approved_submitter_name',
        ),
    ]
