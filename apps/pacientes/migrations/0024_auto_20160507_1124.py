# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0023_auto_20160429_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='numero_documento',
            field=models.CharField(max_length=12, null=True, blank=True),
            preserve_default=True,
        ),
    ]
