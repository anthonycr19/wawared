# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('embarazos', '0031_auto_20171127_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='embarazo',
            name='numero_cigarros_diarios',
            field=models.IntegerField(default=0, verbose_name='Numero de cigarros', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(200)]),
            preserve_default=True,
        ),
    ]
