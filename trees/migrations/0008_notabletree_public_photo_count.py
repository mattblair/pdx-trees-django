# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trees', '0007_photoflag'),
    ]

    operations = [
        migrations.AddField(
            model_name='notabletree',
            name='public_photo_count',
            field=models.IntegerField(default=0),
        ),
    ]
