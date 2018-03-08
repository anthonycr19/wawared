# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0011_auto_20141219_1217'),
    ]

    operations = [
        migrations.AddField(
            model_name='control',
            name='psicoprofilaxis_fecha_1',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='psicoprofilaxis_fecha_2',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='psicoprofilaxis_fecha_3',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='psicoprofilaxis_fecha_4',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='psicoprofilaxis_fecha_5',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='psicoprofilaxis_fecha_6',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
