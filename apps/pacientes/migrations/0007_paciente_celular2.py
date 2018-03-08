# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0006_auto_20141210_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='celular2',
            field=models.IntegerField(null=True, verbose_name='Celular 2', blank=True),
            preserve_default=True,
        ),
    ]
