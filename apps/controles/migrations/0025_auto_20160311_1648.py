# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0024_auto_20160311_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='control',
            name='atencion_fecha',
            field=models.DateField(verbose_name='Fecha de atenci\xf3n'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='control',
            name='atencion_hora',
            field=models.TimeField(verbose_name='Hora de atenci\xf3n'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='control',
            name='zika_departamento',
            field=models.ForeignKey(related_name='zina_departamento', verbose_name='Departameto', blank=True, to='ubigeo.Departamento', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='control',
            name='zika_pais',
            field=models.ForeignKey(related_name='zika_pais', verbose_name='Pa\xeds', blank=True, to='ubigeo.Pais', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='control',
            name='zika_provincia',
            field=models.ForeignKey(related_name='zina_provincia', verbose_name='Provincia', blank=True, to='ubigeo.Provincia', null=True),
            preserve_default=True,
        ),
    ]
