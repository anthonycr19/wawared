# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0040_auto_20170825_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='examenfisico',
            name='tv_membranas_rotas_tiempo',
            field=models.FloatField(blank=True, null=True, verbose_name='Tiempo', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(48)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='examenfisico',
            name='tv_altura_presentacion',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='Altura de presentaci\xf3n', choices=[('0', '5/5 || -4'), ('1', '4/5 || -3'), ('2', '3/5 || -2'), ('3', '2/5 || -1/0'), ('4', '1/5 || +1/+2'), ('5', '0/5 || +3/+4')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='examenfisico',
            name='tv_incorporacion',
            field=models.CharField(blank=True, max_length=20, verbose_name='Incorporaci\xf3n', choices=[('-40%', 'menos de 40%'), ('50%', '50%'), ('70%', '70%'), ('80%', '80%'), ('90%', '90%'), ('100%', '100%')]),
            preserve_default=True,
        ),
    ]
