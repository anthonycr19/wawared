# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0025_vacuna_influenza'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='urbanizacion',
            field=models.CharField(max_length=100, null=True, verbose_name='Sector', blank=True),
            preserve_default=True,
        ),
    ]
