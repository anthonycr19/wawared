# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('embarazos', '0029_auto_20170802_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='planparto',
            name='e3_edad_gestacional',
            field=models.CharField(max_length=10, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='e3_fecha',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='e3_lugar_atencion',
            field=models.CharField(blank=True, max_length=20, choices=[(b'hospital', b'Hospital'), (b'centro salud', b'Centro de salud'), (b'posta salud', b'Posta de salud'), (b'domicilio', b'Domicilio'), (b'no ha decidido', b'No ha decidido'), (b'otros', b'Otros')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='e3_lugar_atencion_otros',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='e3_persona_cuidara_hijos_en_casa',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='e3_persona_que_acompania_en_el_parto',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='e3_posicion_parto',
            field=models.CharField(blank=True, max_length=20, choices=[(b'echada', b'Echada'), (b'cuclillas', b'Cuclillas'), (b'parada', b'Parada'), (b'otros', b'Otros')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='e3_posicion_parto_otros',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='e3_tiempo_llegada_1',
            field=models.SmallIntegerField(null=True, verbose_name='Tiempo de llegada opci\xf3n 1', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='e3_tiempo_llegada_2',
            field=models.SmallIntegerField(null=True, verbose_name='Tiempo de llegada opci\xf3n 2', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='e3_transporte',
            field=models.CharField(blank=True, max_length=20, choices=[(b'taxi', b'Taxi'), (b'mototaxi', b'Mototaxi'), (b'micro', b'Micro'), (b'otros', b'Otros')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='e3_transporte_otros',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='edad_gestacional_elegida',
            field=models.CharField(max_length=20, null=True, verbose_name=b'EG escogida', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='planparto',
            name='e2_transporte',
            field=models.CharField(blank=True, max_length=20, choices=[(b'taxi', b'Taxi'), (b'mototaxi', b'Mototaxi'), (b'micro', b'Micro'), (b'otros', b'Otros')]),
            preserve_default=True,
        ),
    ]
