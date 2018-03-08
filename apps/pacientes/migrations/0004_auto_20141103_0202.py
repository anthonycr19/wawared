# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0003_auto_20141103_0201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='antecedenteginecologico',
            name='ciclo_menstruacion',
            field=models.SmallIntegerField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='antecedenteginecologico',
            name='duracion_menstruacion',
            field=models.SmallIntegerField(default=None, null=True, verbose_name='Duraci\xf3n del ciclo menstrual', blank=True),
            preserve_default=True,
        ),
    ]
