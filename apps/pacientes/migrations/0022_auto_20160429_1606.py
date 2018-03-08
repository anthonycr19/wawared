# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0021_auto_20160429_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='categorizacion',
            field=models.CharField(max_length=50, null=True, verbose_name='Categorizaci\xf3n', choices=[(b'anexo', b'Anexo'), (b'asentamientos humanos', b'Asentamientos Humanos'), (b'asociacion de vivienda', 'Asociaci\xf3n de vivienda'), (b'barrio o cuartel', b'Barrio o cuartel'), (b'campamento minero', b'Campamento minero'), (b'caserio', b'Caserio'), (b'ciudad', b'Ciudad'), (b'comunidad campesina', b'Comunidad campesina'), (b'comunidad indigena', 'Comunidad Ind\xedgena'), (b'conjunto habitacional', b'Conjunto Habitacional'), (b'cooperativa agraria de produccion', 'Cooperativa agraria de producci\xf3n'), (b'cooperativa de vivienda', b'Cooperativa de vivienda'), (b'pueblo joven', b'Pueblo Joven'), (b'pueblo', b'Pueblo'), (b'unidad agropecuaria', b'Unidad Agropecuaria'), (b'urbanizacion', 'Urbanizaci\xf3n')]),
            preserve_default=True,
        ),
    ]
