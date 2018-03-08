# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partos', '0008_placenta_liquido_amniotico_otras_caracteristicas'),
        ('controles', '0044_auto_20171110_0000'),
    ]

    operations = [
        migrations.AddField(
            model_name='control',
            name='oc_lactancia_materna',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='diagnosticodetalle',
            name='diagnostico_embarazo',
            field=models.ForeignKey(related_name='detalles_puerperio', blank=True, to='partos.TerminacionEmbarazo', null=True),
            preserve_default=True,
        ),
    ]
