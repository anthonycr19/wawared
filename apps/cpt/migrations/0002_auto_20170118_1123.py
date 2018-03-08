# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cpt', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='catalogoprocedimiento',
            name='codigo_grupo',
        ),
        migrations.RemoveField(
            model_name='catalogoprocedimiento',
            name='codigo_seccion',
        ),
        migrations.RemoveField(
            model_name='catalogoprocedimiento',
            name='codigo_subseccion',
        ),
        migrations.RemoveField(
            model_name='catalogoprocedimiento',
            name='descripcion_seccion',
        ),
        migrations.RemoveField(
            model_name='catalogoprocedimiento',
            name='nombre_grupo',
        ),
        migrations.RemoveField(
            model_name='catalogoprocedimiento',
            name='subdivision_anatomica',
        ),
        migrations.AddField(
            model_name='catalogoprocedimiento',
            name='sexo',
            field=models.CharField(default=None, max_length=1, null=True, blank=True, choices=[(None, b'No determinado'), (b'F', b'Femenino'), (b'M', b'Masculino')]),
            preserve_default=True,
        ),
    ]
