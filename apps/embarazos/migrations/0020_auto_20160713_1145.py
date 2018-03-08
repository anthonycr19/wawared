# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('embarazos', '0019_auto_20160621_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='embarazo',
            name='padre_apellido_materno',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Apellido materno del padre', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='embarazo',
            name='padre_apellido_paterno',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Apellido paterno del padre', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='embarazo',
            name='padre_nombres',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Nombres del padre', blank=True),
            preserve_default=True,
        ),
    ]
