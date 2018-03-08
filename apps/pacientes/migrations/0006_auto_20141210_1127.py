# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0005_auto_20141126_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='estado_civil',
            field=models.CharField(max_length=20, null=True, verbose_name='Estado Civil', choices=[(b'soltera', 'Soltera'), (b'conviviente', 'Conviviente'), (b'casada', 'Casada'), (b'divorciada', 'Divorciada'), (b'viuda', 'Viuda')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paciente',
            name='estudio',
            field=models.ForeignKey(to='pacientes.Estudio', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paciente',
            name='etnia',
            field=models.ForeignKey(to='pacientes.Etnia', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paciente',
            name='ocupacion',
            field=models.ForeignKey(to='pacientes.Ocupacion', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paciente',
            name='tiempo_estudio',
            field=models.SmallIntegerField(null=True, verbose_name='A\xf1os aprobados', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)]),
            preserve_default=True,
        ),
    ]
