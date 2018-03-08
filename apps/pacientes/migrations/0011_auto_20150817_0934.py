# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pacientes.models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0010_paciente_categorizacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historiaclinica',
            name='numero',
            field=models.CharField(max_length=20, validators=[pacientes.models.validate_hc_length]),
            preserve_default=True,
        ),
    ]
