# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trees', '0009_auto_20150601_0929'),
    ]

    operations = [
        migrations.AddField(
            model_name='treephoto',
            name='license',
            field=models.CharField(default=b'CC BY-SA', max_length=20, choices=[(b'CC BY-SA', b'CC Attribution-ShareAlike'), (b'CC BY', b'CC Attribution'), (b'CC BY-NC-SA', b'CC Attribution-NonCommercial-ShareAlike'), (b'Public Domain', b'Public Domain'), (b'Unknown', b'Unknown')]),
        ),
    ]
