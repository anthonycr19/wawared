# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0011_auto_20150817_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='celular',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Celular 1', validators=[django.core.validators.RegexValidator(b'^\\d{9}$', 'Ingrese un n\xfamero valido(9 digitos sin espacios)')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paciente',
            name='celular2',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Celular 2', validators=[django.core.validators.RegexValidator(b'^\\d{9}$', 'Ingrese un n\xfamero valido(9 digitos sin espacios)')]),
            preserve_default=True,
        ),
    ]
