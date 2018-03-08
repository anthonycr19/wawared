# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0015_auto_20160317_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='numero_documento',
            field=models.CharField(max_length=12, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paciente',
            name='tipo_documento',
            field=models.CharField(default=b'dni', max_length=10, verbose_name='Tipo Documento', choices=[(b'dni', 'DNI'), (b'pasaporte', 'Pasaporte'), (b'ce', 'CE'), (b'nie', 'CIE'), (b'nodoc', 'Indocumentado')]),
            preserve_default=True,
        ),
    ]
