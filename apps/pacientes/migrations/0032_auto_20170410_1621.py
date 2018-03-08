# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0031_auto_20170410_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='departamento_residencia',
            field=models.ForeignKey(related_name='residencia_pacientes', to='ubigeo.Departamento', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paciente',
            name='provincia_residencia',
            field=models.ForeignKey(related_name='residencia_pacientes', to='ubigeo.Provincia', null=True),
            preserve_default=True,
        ),
    ]
