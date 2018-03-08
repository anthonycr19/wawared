# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0019_auto_20160426_0842'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='paciente',
            unique_together=set([('tipo_documento', 'numero_documento', 'dni_responsable')]),
        ),
    ]
