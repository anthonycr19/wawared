# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0007_paciente_celular2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='celular',
            field=models.IntegerField(null=True, verbose_name='Celular 1', blank=True),
            preserve_default=True,
        ),
    ]
