# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('embarazos', '0014_embarazo_fecha_tamizaje'),
    ]

    operations = [
        migrations.AlterField(
            model_name='embarazo',
            name='depresion_puntaje',
            field=models.SmallIntegerField(default=None, null=True, verbose_name=b'Puntaje', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fichaproblema',
            name='alimenticio',
            field=models.CharField(blank=True, max_length=50, null=True, choices=[(b'0', b'Nunca'), (b'1', b'Varios dias'), (b'2', b'Mas de las mitad de los dias'), (b'3', b'Casi todos los dias')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fichaproblema',
            name='cansancio',
            field=models.CharField(blank=True, max_length=50, null=True, choices=[(b'0', b'Nunca'), (b'1', b'Varios dias'), (b'2', b'Mas de las mitad de los dias'), (b'3', b'Casi todos los dias')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fichaproblema',
            name='desanimada_deprimida',
            field=models.CharField(blank=True, max_length=50, null=True, choices=[(b'0', b'Nunca'), (b'1', b'Varios dias'), (b'2', b'Mas de las mitad de los dias'), (b'3', b'Casi todos los dias')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fichaproblema',
            name='dificultad_concentracion',
            field=models.CharField(blank=True, max_length=50, null=True, choices=[(b'0', b'Nunca'), (b'1', b'Varios dias'), (b'2', b'Mas de las mitad de los dias'), (b'3', b'Casi todos los dias')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fichaproblema',
            name='difucultad_cumplir_labores',
            field=models.CharField(blank=True, max_length=50, null=True, choices=[(b'nada en absoluto', b'Nada en absoluto'), (b'algo dificil', b'Algo dificil'), (b'muy dificil', b'Muy dificil'), (b'extremadamente dificil', b'Extremadamente dificil')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fichaproblema',
            name='falta_autoestima',
            field=models.CharField(blank=True, max_length=50, null=True, choices=[(b'0', b'Nunca'), (b'1', b'Varios dias'), (b'2', b'Mas de las mitad de los dias'), (b'3', b'Casi todos los dias')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fichaproblema',
            name='mueve_lento_o_hiperactivo',
            field=models.CharField(blank=True, max_length=50, null=True, choices=[(b'0', b'Nunca'), (b'1', b'Varios dias'), (b'2', b'Mas de las mitad de los dias'), (b'3', b'Casi todos los dias')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fichaproblema',
            name='pensamientos_autodestructivos',
            field=models.CharField(blank=True, max_length=50, null=True, choices=[(b'0', b'Nunca'), (b'1', b'Varios dias'), (b'2', b'Mas de las mitad de los dias'), (b'3', b'Casi todos los dias')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fichaproblema',
            name='poco_interes_o_placer',
            field=models.CharField(blank=True, max_length=50, null=True, choices=[(b'0', b'Nunca'), (b'1', b'Varios dias'), (b'2', b'Mas de las mitad de los dias'), (b'3', b'Casi todos los dias')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fichaproblema',
            name='problemas_dormir',
            field=models.CharField(blank=True, max_length=50, null=True, choices=[(b'0', b'Nunca'), (b'1', b'Varios dias'), (b'2', b'Mas de las mitad de los dias'), (b'3', b'Casi todos los dias')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fichaproblema',
            name='puntaje',
            field=models.SmallIntegerField(null=True, verbose_name=b'Puntaje', blank=True),
            preserve_default=True,
        ),
    ]
