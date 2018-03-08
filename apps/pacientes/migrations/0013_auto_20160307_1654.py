# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0012_auto_20151030_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='tipo_documento',
            field=models.CharField(default=b'dni', max_length=10, verbose_name='Tipo Documento', choices=[(b'dni', 'DNI'), (b'pasaporte', 'Pasaporte'), (b'ce', 'CE'), (b'nie', 'NIE'), (b'indocumentado', 'Indocumentado')]),
            preserve_default=True,
        ),
    ]
