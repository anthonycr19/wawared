# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('establecimientos', '0002_auto_20141106_1624'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='establecimiento',
            options={'verbose_name': 'Establecimiento', 'verbose_name_plural': 'Establecimientos', 'permissions': (('download_reporte_global', 'Descargar reporte global'), ('download_reporte_sien', 'Descargar reporte SIEN'), ('download_reporte_registro_diario_gestaciones', 'Descargar registro diario de gestaciones'))},
        ),
    ]
