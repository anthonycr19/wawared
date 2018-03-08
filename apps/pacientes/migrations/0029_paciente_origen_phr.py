# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0028_auto_20170124_1049'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='origen_phr',
            field=models.BooleanField(default=False, verbose_name='Phr'),
            preserve_default=True,
        ),
    ]
