# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0018_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='operador',
            field=models.CharField(default=b'movistar', max_length=10, verbose_name='Compa\xf1ia Celular', choices=[(b'movistar', 'Movistar'), (b'claro', 'Claro'), (b'entel', 'Entel'), (b'bitel', 'Bitel')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paciente',
            name='tipo_documento',
            field=models.CharField(default=b'dni', max_length=10, verbose_name='Tipo Documento', choices=[(b'dni', 'DNI'), (b'pasaporte', 'Pasaporte'), (b'ce', 'CE'), (b'nie', 'DIE'), (b'nodoc', 'Indocumentado')]),
            preserve_default=True,
        ),
    ]
