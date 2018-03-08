# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0027_auto_20170112_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='tipo_documento',
            field=models.CharField(default=b'dni', max_length=20, verbose_name='Tipo Documento', choices=[(b'dni', 'DNI'), (b'le', 'LIBRETA ELECTORAL'), (b'lm', 'LIBRETA MILITAR'), (b'boleta', 'BOLETA DE INSCRIPCION'), (b'partidanacimiento', 'PARTIDA DE NACIMIENTO'), (b'carnetidentidad', 'CARNET DE IDENTIDAD'), (b'brevete', 'BREVETE'), (b'ce', 'CE'), (b'pasaporte', 'Pasaporte'), (b'carnetuniversitario', 'CARNET UNIVERSITARIO'), (b'nie', 'DIE'), (b'noespecifica', 'SIN ESPECIFICACION'), (b'notrajo', 'NO TRAJO DOCUMENTO'), (b'nodoc', 'Indocumentado')]),
            preserve_default=True,
        ),
    ]
