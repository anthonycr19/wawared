# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0014_auto_20150116_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnostico',
            name='examen_factor',
            field=models.BooleanField(default=False, verbose_name='Factor'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='diagnostico',
            name='examen_glucosa',
            field=models.BooleanField(default=False, verbose_name='Glucosa'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='diagnostico',
            name='examen_grupo_sanguineo',
            field=models.BooleanField(default=False, verbose_name='Grupo sanguineo'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='diagnostico',
            name='examen_hemoglobina',
            field=models.BooleanField(default=False, verbose_name='Hemoglobina'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='diagnostico',
            name='examen_hemograma',
            field=models.BooleanField(default=False, verbose_name='Hemograma'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='diagnostico',
            name='examen_orina',
            field=models.BooleanField(default=False, verbose_name='Orina'),
            preserve_default=True,
        ),
    ]
