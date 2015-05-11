# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trees', '0005_auto_20150505_1217'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='treephoto',
            options={'ordering': ['-display_order', 'submitted_date']},
        ),
        migrations.AddField(
            model_name='treephoto',
            name='display_order',
            field=models.IntegerField(default=50, help_text=b'Higher values will be displayed first.'),
        ),
    ]
