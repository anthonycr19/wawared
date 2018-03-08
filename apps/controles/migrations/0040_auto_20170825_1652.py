# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0039_auto_20170519_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='control',
            name='fua_identificador_envio_trama',
            field=models.IntegerField(max_length=3, null=True, verbose_name='FCF', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='fua_numero_asiganado',
            field=models.CharField(max_length=15, null=True, verbose_name='Numero formato FUA generado', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='control',
            name='istramafua',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
    ]
