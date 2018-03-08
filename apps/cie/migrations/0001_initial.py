# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ICD10Base',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(unique=True, max_length=6, verbose_name='C\xf3digo', db_index=True)),
                ('nombre', models.CharField(max_length=256, verbose_name='Nombre')),
                ('nombre_mostrar', models.CharField(max_length=256, verbose_name='Nombre mostrar', blank=True)),
                ('is_activo', models.BooleanField(default=True)),
                ('is_familia', models.BooleanField(default=True)),
                ('is_medico', models.BooleanField(default=True)),
                ('is_icd10', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ICD10',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('cie.icd10base',),
        ),
        migrations.CreateModel(
            name='ICD10Medical',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('cie.icd10base',),
        ),
    ]
