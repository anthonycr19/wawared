# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0016_auto_20150407_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examenfisico',
            name='tv_altura_presentacion',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='Altura de presentaci\xf3n', choices=[('1', '+1 / -4'), ('2', '+2 / -3'), ('3', '+3 / -2'), ('4', '+4 / -1'), ('5', '+5 / 0')]),
            preserve_default=True,
        ),
    ]
