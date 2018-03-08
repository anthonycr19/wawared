# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0038_auto_20170503_1256'),
    ]

    operations = [
        migrations.AddField(
            model_name='control',
            name='visita_domiciliaria_actividad_1',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='visita_domiciliaria_actividad_2',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='visita_domiciliaria_actividad_3',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='visita_domiciliaria_actividad_4',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='visita_domiciliaria_actividad_5',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='visita_domiciliaria_actividad_6',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='visita_domiciliaria_fecha_1',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='visita_domiciliaria_fecha_2',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='visita_domiciliaria_fecha_3',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='visita_domiciliaria_fecha_4',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='visita_domiciliaria_fecha_5',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='visita_domiciliaria_fecha_6',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='control',
            name='frecuencia_respiratoria',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Frecuencia respiratoria', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(180)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='control',
            name='presion_diastolica',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Presion diastolica', validators=[django.core.validators.MinValueValidator(40), django.core.validators.MaxValueValidator(200)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='control',
            name='presion_sistolica',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Presion sistolica', validators=[django.core.validators.MinValueValidator(50), django.core.validators.MaxValueValidator(300)]),
            preserve_default=True,
        ),
    ]
