# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('embarazos', '0005_planparto_e2_lugar_atencion_observacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='embarazo',
            name='violencia_familiar',
        ),
        migrations.RemoveField(
            model_name='fichaviolenciafamiliar',
            name='agresores',
        ),
        migrations.AddField(
            model_name='fichaviolenciafamiliar',
            name='violencia_fisica',
            field=models.NullBooleanField(default=None),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fichaviolenciafamiliar',
            name='violencia_fisica_agresores',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fichaviolenciafamiliar',
            name='violencia_psicologica',
            field=models.NullBooleanField(default=None),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fichaviolenciafamiliar',
            name='violencia_psicologica_agresores',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fichaviolenciafamiliar',
            name='violencia_sexual',
            field=models.NullBooleanField(default=None),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fichaviolenciafamiliar',
            name='violencia_sexual_agresores',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
    ]
