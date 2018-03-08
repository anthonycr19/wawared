# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('embarazos', '0021_auto_20160915_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bebe',
            name='peso',
            field=models.FloatField(default=0, null=True),
            preserve_default=True,
        ),
    ]
