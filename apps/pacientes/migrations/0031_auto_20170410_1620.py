# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0030_auto_20170323_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='distrito_residencia',
            field=models.ForeignKey(related_name='residencia_pacientes', to='ubigeo.Distrito', null=True),
            preserve_default=True,
        ),
    ]
