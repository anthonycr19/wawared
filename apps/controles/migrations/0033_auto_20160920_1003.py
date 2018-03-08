# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partos', '0001_initial'),
        ('controles', '0032_auto_20160915_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='examenfisico',
            name='ingreso',
            field=models.OneToOneField(related_name='examen_fisico', null=True, blank=True, to='partos.Ingreso'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sintoma',
            name='ingreso',
            field=models.ForeignKey(related_name='sintomas_ingreso', blank=True, to='partos.Ingreso', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='examenfisico',
            name='control',
            field=models.OneToOneField(related_name='examen_fisico', null=True, blank=True, to='controles.Control'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sintoma',
            name='control',
            field=models.ForeignKey(related_name='sintomas', blank=True, to='controles.Control', null=True),
            preserve_default=True,
        ),
    ]
