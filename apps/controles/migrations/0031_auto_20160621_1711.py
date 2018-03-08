# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0030_auto_20160601_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='laboratorio',
            name='pcr_zika',
            field=models.CharField(default='no aplica', max_length=20, verbose_name='PCR Zika', choices=[('positivo', 'Positivo'), ('negativo', 'Negativo'), ('no se hizo', 'No se hizo'), ('no aplica', 'No aplica')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='laboratorio',
            name='pcr_zika_fecha',
            field=models.DateField(null=True, verbose_name='Fecha', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='laboratorio',
            name='pcr_zika_observacion',
            field=models.CharField(max_length=200, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
    ]
