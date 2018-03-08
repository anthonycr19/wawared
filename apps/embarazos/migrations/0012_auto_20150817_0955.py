# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('embarazos', '0011_auto_20150406_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='embarazo',
            name='padre_apellido_materno',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Padre apellido materno', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='embarazo',
            name='padre_apellido_paterno',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Padre apellido paterno', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='embarazo',
            name='padre_nombres',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Padre nombres', blank=True),
            preserve_default=True,
        ),
    ]
