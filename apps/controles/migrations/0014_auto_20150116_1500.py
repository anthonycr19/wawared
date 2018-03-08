# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0013_auto_20150116_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='control',
            name='indicacion_hierro_acido_folico',
            field=models.IntegerField(blank=True, null=True, verbose_name='Indicaci\xf3n de Sulfato Ferroso/Ac F\xf3lico (mayor o igual a 14 semanas)', validators=[django.core.validators.MinValueValidator(5), django.core.validators.MaxValueValidator(100)]),
            preserve_default=True,
        ),
    ]
