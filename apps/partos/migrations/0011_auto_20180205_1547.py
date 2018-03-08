# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('partos', '0010_auto_20171127_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingreso',
            name='tiempo_ruptura_membranas_horas',
            field=models.IntegerField(blank=True, null=True, verbose_name='Tiempo horas', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(48)]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ingreso',
            name='tiempo_ruptura_membranas_minutos',
            field=models.IntegerField(blank=True, null=True, verbose_name='Tiempo minutos', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(60)]),
            preserve_default=True,
        ),
    ]
