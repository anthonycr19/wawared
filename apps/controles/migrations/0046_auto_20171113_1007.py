# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0045_auto_20171113_1007'),
        ('puerperio', '0002_auto_20171113_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagnosticodetalle',
            name='diagnostico_puerperio',
            field=models.ForeignKey(related_name='detalles_puerperio', blank=True, to='puerperio.TerminacionPuerpera', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='laboratorio',
            name='hemoglobina_3',
            field=models.NullBooleanField(default=None, verbose_name='Hemoglobina 3'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='laboratorio',
            name='hemoglobina_3_fecha',
            field=models.DateField(null=True, verbose_name='Fecha', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='laboratorio',
            name='hemoglobina_3_resultado',
            field=models.FloatField(default=None, null=True, verbose_name='Hemoglobina 3 resultado', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='laboratorio',
            name='hemoglobina_4',
            field=models.NullBooleanField(default=None, verbose_name='Hemoglobina 4'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='laboratorio',
            name='hemoglobina_4_fecha',
            field=models.DateField(null=True, verbose_name='Fecha', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='laboratorio',
            name='hemoglobina_4_resultado',
            field=models.FloatField(default=None, null=True, verbose_name='Hemoglobina 4 resultado', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='laboratorio',
            name='hemoglobina_5',
            field=models.NullBooleanField(default=None, verbose_name='Hemoglobina 5'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='laboratorio',
            name='hemoglobina_5_fecha',
            field=models.DateField(null=True, verbose_name='Fecha', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='laboratorio',
            name='hemoglobina_5_resultado',
            field=models.FloatField(default=None, null=True, verbose_name='Hemoglobina 5 resultado', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='laboratorio',
            name='rapida_proteinuria_2',
            field=models.CharField(default='no se hizo', choices=[('reactivo', 'Reactivo'), ('no reactivo', 'No reactivo'), ('no se hizo', 'No se hizo')], max_length=20, blank=True, null=True, verbose_name='Prueba r\xe1pida de Proteinuria 2'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='laboratorio',
            name='rapida_proteinuria_3',
            field=models.CharField(default='no se hizo', choices=[('reactivo', 'Reactivo'), ('no reactivo', 'No reactivo'), ('no se hizo', 'No se hizo')], max_length=20, blank=True, null=True, verbose_name='Prueba r\xe1pida de Proteinuria 3'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='laboratorio',
            name='rapida_proteinuria_fecha_2',
            field=models.DateField(null=True, verbose_name='Fecha', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='laboratorio',
            name='rapida_proteinuria_fecha_3',
            field=models.DateField(null=True, verbose_name='Fecha', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='laboratorio',
            name='rapida_proteinuria_observacion_2',
            field=models.CharField(max_length=200, null=True, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='laboratorio',
            name='rapida_proteinuria_observacion_3',
            field=models.CharField(max_length=200, null=True, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='diagnosticodetalle',
            name='diagnostico',
            field=models.ForeignKey(related_name='detalles', blank=True, to='controles.Diagnostico', null=True),
            preserve_default=True,
        ),
    ]
