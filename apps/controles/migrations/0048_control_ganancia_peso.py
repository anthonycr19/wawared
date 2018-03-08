# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0047_control_oc_signos_alarma'),
    ]

    operations = [
        migrations.AddField(
            model_name='control',
            name='ganancia_peso',
            field=models.FloatField(null=True, verbose_name='Ganancia de peso', blank=True),
            preserve_default=True,
        ),
    ]
