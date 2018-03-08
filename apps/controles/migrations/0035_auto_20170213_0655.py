# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0034_procedimientodetalle'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='control',
            unique_together=set([('embarazo', 'establecimiento', 'paciente', 'atencion_fecha', 'atencion_hora')]),
        ),
    ]
