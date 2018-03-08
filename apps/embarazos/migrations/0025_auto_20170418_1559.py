# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('embarazos', '0024_bebe_no_recuerda_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bebe',
            name='fecha',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bebe',
            name='no_recuerda_fecha',
            field=models.BooleanField(default=False, verbose_name=''),
            preserve_default=True,
        ),
    ]
