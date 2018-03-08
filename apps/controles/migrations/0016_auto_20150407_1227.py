# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0015_auto_20150310_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examenfisico',
            name='tv_altura_presentacion',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Altura de presentaci\xf3n', choices=[('1', '+1 / -4'), ('2', '+2 / -3'), ('3', '+3 / -2'), ('4', '+4 / -1'), ('5', '+5 / 0')]),
            preserve_default=True,
        ),
    ]
