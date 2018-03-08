# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('embarazos', '0004_auto_20150103_2204'),
    ]

    operations = [
        migrations.AddField(
            model_name='planparto',
            name='e2_lugar_atencion_observacion',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
