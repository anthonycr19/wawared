# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('embarazos', '0010_auto_20150406_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='embarazo',
            name='depresion_puntaje',
            field=models.SmallIntegerField(default=0, verbose_name=b'Puntaje'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fichaproblema',
            name='puntaje',
            field=models.SmallIntegerField(default=0, verbose_name=b'Puntaje'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fichaproblema',
            name='alimenticio',
            field=models.CharField(default=b'0', max_length=50, choices=[(b'0', b'Nunca'), (b'1', b'Varios dias'), (b'2', b'Mas de las mitad de los dias'), (b'3', b'Casi todos los dias')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fichaproblema',
            name='cansancio',
            field=models.CharField(default=b'0', max_length=50, choices=[(b'0', b'Nunca'), (b'1', b'Varios dias'), (b'2', b'Mas de las mitad de los dias'), (b'3', b'Casi todos los dias')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fichaproblema',
            name='desanimada_deprimida',
            field=models.CharField(default=b'0', max_length=50, choices=[(b'0', b'Nunca'), (b'1', b'Varios dias'), (b'2', b'Mas de las mitad de los dias'), (b'3', b'Casi todos los dias')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fichaproblema',
            name='dificultad_concentracion',
            field=models.CharField(default=b'0', max_length=50, choices=[(b'0', b'Nunca'), (b'1', b'Varios dias'), (b'2', b'Mas de las mitad de los dias'), (b'3', b'Casi todos los dias')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fichaproblema',
            name='falta_autoestima',
            field=models.CharField(default=b'0', max_length=50, choices=[(b'0', b'Nunca'), (b'1', b'Varios dias'), (b'2', b'Mas de las mitad de los dias'), (b'3', b'Casi todos los dias')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fichaproblema',
            name='mueve_lento_o_hiperactivo',
            field=models.CharField(default=b'0', max_length=50, null=True, blank=True, choices=[(b'0', b'Nunca'), (b'1', b'Varios dias'), (b'2', b'Mas de las mitad de los dias'), (b'3', b'Casi todos los dias')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fichaproblema',
            name='pensamientos_autodestructivos',
            field=models.CharField(default=b'0', max_length=50, choices=[(b'0', b'Nunca'), (b'1', b'Varios dias'), (b'2', b'Mas de las mitad de los dias'), (b'3', b'Casi todos los dias')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fichaproblema',
            name='poco_interes_o_placer',
            field=models.CharField(default=b'0', max_length=50, choices=[(b'0', b'Nunca'), (b'1', b'Varios dias'), (b'2', b'Mas de las mitad de los dias'), (b'3', b'Casi todos los dias')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fichaproblema',
            name='problemas_dormir',
            field=models.CharField(default=b'0', max_length=50, choices=[(b'0', b'Nunca'), (b'1', b'Varios dias'), (b'2', b'Mas de las mitad de los dias'), (b'3', b'Casi todos los dias')]),
            preserve_default=True,
        ),
    ]
