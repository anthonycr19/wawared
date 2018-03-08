# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0021_diagnostico_tratamiento_2'),
    ]

    operations = [
        migrations.AddField(
            model_name='laboratorio',
            name='rapida_proteinuria',
            field=models.CharField(default='no se hizo', choices=[('reactivo', 'Reactivo'), ('no reactivo', 'No reactivo'), ('no se hizo', 'No se hizo')], max_length=20, blank=True, null=True, verbose_name='Prueba r\xe1pida de Proteinuria'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='laboratorio',
            name='rapida_proteinuria_fecha',
            field=models.DateField(null=True, verbose_name='Fecha', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='laboratorio',
            name='rapida_proteinuria_observacion',
            field=models.CharField(max_length=200, null=True, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
    ]
