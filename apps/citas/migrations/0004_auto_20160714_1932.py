# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0003_cita_fecha_asistio'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cita',
            unique_together=set([('fecha', 'establecimiento', 'paciente')]),
        ),
    ]
