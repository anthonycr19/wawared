# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0012_auto_20141219_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnostico',
            name='examen_factor',
            field=models.BooleanField(default=True, verbose_name='Factor'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='diagnostico',
            name='examen_glucosa',
            field=models.BooleanField(default=True, verbose_name='Glucosa'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='diagnostico',
            name='examen_grupo_sanguineo',
            field=models.BooleanField(default=True, verbose_name='Grupo sanguineo'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='diagnostico',
            name='examen_hemoglobina',
            field=models.BooleanField(default=True, verbose_name='Hemoglobina'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='diagnostico',
            name='examen_hemograma',
            field=models.BooleanField(default=True, verbose_name='Hemograma'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='diagnostico',
            name='examen_orina',
            field=models.BooleanField(default=True, verbose_name='Orina'),
            preserve_default=True,
        ),
    ]
