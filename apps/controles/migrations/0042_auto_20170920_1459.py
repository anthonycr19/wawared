# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partos', '0005_auto_20170920_1459'),
        ('controles', '0041_auto_20170915_0920'),
    ]

    operations = [
        migrations.AddField(
            model_name='examenfisicofetal',
            name='ingreso_parto',
            field=models.ForeignKey(blank=True, to='partos.Ingreso', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='examenfisicofetal',
            name='medicion_parto',
            field=models.ForeignKey(blank=True, to='partos.PartogramaMedicion', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='examenfisicofetal',
            name='control',
            field=models.ForeignKey(related_name='control', blank=True, to='controles.Control', null=True),
            preserve_default=True,
        ),
    ]
