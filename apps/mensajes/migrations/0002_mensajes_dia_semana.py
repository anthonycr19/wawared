# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('mensajes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mensajes',
            name='dia_semana',
            field=models.IntegerField(default=0, choices=[(0, 'Lunes'), (1, 'Martes'), (2, 'Miercoles'), (3, 'Jueves'), (4, 'Viernes'), (5, 'Sabado'), (6, 'Domingo')], verbose_name='Dia de semana', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(6)]),
            preserve_default=True,
        ),
    ]
