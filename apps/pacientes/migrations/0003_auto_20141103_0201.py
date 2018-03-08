# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0002_auto_20141103_0140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='antecedenteginecologico',
            name='andria',
            field=models.SmallIntegerField(default=None, null=True, verbose_name='Andria', blank=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='antecedenteginecologico',
            name='edad_menarquia',
            field=models.SmallIntegerField(default=None, null=True, verbose_name='Menarquia edad', blank=True, validators=[django.core.validators.MinValueValidator(8), django.core.validators.MaxValueValidator(20)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='antecedenteginecologico',
            name='edad_primera_relacion_sexual',
            field=models.SmallIntegerField(default=None, null=True, verbose_name='Edad primera relacion sexual', blank=True),
            preserve_default=True,
        ),
    ]
