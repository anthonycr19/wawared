# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CatalogoProcedimiento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo_grupo', models.CharField(max_length=10)),
                ('nombre_grupo', models.CharField(max_length=200)),
                ('codigo_seccion', models.CharField(max_length=10, null=True, blank=True)),
                ('descripcion_seccion', models.CharField(max_length=200, null=True, blank=True)),
                ('codigo_subseccion', models.CharField(max_length=10, null=True, blank=True)),
                ('subdivision_anatomica', models.CharField(max_length=200, null=True, blank=True)),
                ('codigo_cpt', models.CharField(max_length=20, null=True, blank=True)),
                ('denominacion_procedimientos', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
