# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mensajes', '0002_mensajes_dia_semana'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='mensajes',
            unique_together=set([('semana_mensaje', 'dia_semana', 'tipo_mensaje')]),
        ),
    ]
