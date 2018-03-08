# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('embarazos', '0021_auto_20160915_1100'),
        ('pacientes', '0026_auto_20160713_1108'),
        ('controles', '0031_auto_20160621_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='laboratorio',
            name='embarazo',
            field=models.ForeignKey(related_name='laboratorios', blank=True, to='embarazos.Embarazo', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='laboratorio',
            name='paciente',
            field=models.ForeignKey(related_name='laboratorios', blank=True, to='pacientes.Paciente', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='control',
            name='posicion',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Posicion', choices=[('d', 'Derecho'), ('i', 'Izquierdo'), ('na', 'Indiferente')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='control',
            name='presentacion',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Presentacion', choices=[('c', 'Cefalico'), ('p', 'Podalico'), ('na', 'Indiferente')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='control',
            name='situacion',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Situacion', choices=[('l', 'Longitudinal'), ('t', 'Transversal'), ('na', 'Indiferente')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='control',
            field=models.OneToOneField(related_name='laboratorio', null=True, blank=True, to='controles.Control'),
            preserve_default=True,
        ),
    ]
