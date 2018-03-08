# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0009_paciente_codigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='categorizacion',
            field=models.CharField(max_length=50, null=True, verbose_name='Categorizaci\xf3n', choices=[(b'ciudad', b'Ciudad'), (b'pueblo joven', b'Pueblo Joven'), (b'conjunto habitacional', b'Conjunto Habitacional'), (b'asociacion de vivienda', 'Asociaci\xf3n de vivienda'), (b'cooperativa de vivienda', b'Cooperativa de vivienda'), (b'barrio o cuartel', b'Barrio o cuartel'), (b'pueblo', b'Pueblo'), (b'caserio', b'Caserio'), (b'anexo', b'Anexo'), (b'comunidad indigena', 'Comunidad Ind\xedgena'), (b'unidad agropecuaria', b'Unidad Agropecuaria'), (b'cooperativa agraria de produccion', 'Cooperativa agraria de producci\xf3n'), (b'comunidad campesina', b'Comunidad campesina'), (b'campamento minero', b'Campamento minero')]),
            preserve_default=True,
        ),
    ]
