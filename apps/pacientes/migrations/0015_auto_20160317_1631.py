# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0014_auto_20160310_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='categorizacion',
            field=models.CharField(max_length=50, null=True, verbose_name='Categorizaci\xf3n', choices=[(b'anexo', b'Anexo'), (b'asociacion de vivienda', 'Asociaci\xf3n de vivienda'), (b'barrio o cuartel', b'Barrio o cuartel'), (b'campamento minero', b'Campamento minero'), (b'caserio', b'Caserio'), (b'ciudad', b'Ciudad'), (b'comunidad campesina', b'Comunidad campesina'), (b'comunidad indigena', 'Comunidad Ind\xedgena'), (b'conjunto habitacional', b'Conjunto Habitacional'), (b'cooperativa agraria de produccion', 'Cooperativa agraria de producci\xf3n'), (b'cooperativa de vivienda', b'Cooperativa de vivienda'), (b'pueblo joven', b'Pueblo Joven'), (b'pueblo', b'Pueblo'), (b'unidad agropecuaria', b'Unidad Agropecuaria'), (b'urbanizacion', 'Urbanizaci\xf3n')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paciente',
            name='operador',
            field=models.CharField(default=b'movistar', max_length=10, verbose_name='Compa\xf1ia Celular', choices=[(b'movistar', 'Movistar'), (b'claro', 'Claro'), (b'nextel', 'Nextel'), (b'bitel', 'Bitel')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paciente',
            name='tipo_documento',
            field=models.CharField(default=b'dni', max_length=10, verbose_name='Tipo Documento', choices=[(b'dni', 'DNI'), (b'pasaporte', 'Pasaporte'), (b'ce', 'CE'), (b'nie', 'CIE'), (b'indocumentado', 'Indocumentado')]),
            preserve_default=True,
        ),
    ]
