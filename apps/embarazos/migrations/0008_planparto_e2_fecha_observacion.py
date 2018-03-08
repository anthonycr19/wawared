# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('embarazos', '0007_auto_20150104_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='planparto',
            name='e2_fecha_observacion',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
