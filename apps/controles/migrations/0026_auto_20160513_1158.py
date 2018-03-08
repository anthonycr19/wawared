# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controles', '0025_auto_20160311_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examenfisico',
            name='eg_posicion',
            field=models.CharField(default='n/a', max_length=20, verbose_name='Posici\xf3n', blank=True, choices=[('anteversoflexo', 'Anteversoflexo'), ('medio', 'Medio'), ('retroversoflexo', 'Retroversoflexo'), ('n/a', 'N/A')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='examenfisico',
            name='pelvimetria_observacion',
            field=models.CharField(max_length=100, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='bk_en_esputo_observacion',
            field=models.CharField(max_length=200, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='colposcopia_observacion',
            field=models.CharField(max_length=200, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='elisa_observacion',
            field=models.CharField(max_length=200, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='examen_completo_orina_observacion_1',
            field=models.CharField(max_length=200, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='examen_completo_orina_observacion_2',
            field=models.CharField(max_length=200, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='fluorencia_malaria_observacion',
            field=models.CharField(max_length=200, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='fta_abs_observacion',
            field=models.CharField(max_length=200, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='glicemia_1_observacion',
            field=models.CharField(max_length=200, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='glicemia_2_observacion',
            field=models.CharField(max_length=200, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='gota_gruesa_observacion',
            field=models.CharField(max_length=200, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='htlv_1_observacion',
            field=models.CharField(max_length=200, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='ifi_western_blot_observacion',
            field=models.CharField(max_length=200, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='iva_observacion',
            field=models.CharField(max_length=200, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='leucocituria_observacion',
            field=models.CharField(max_length=200, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='listeria_observacion',
            field=models.CharField(max_length=200, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='malaria_prueba_rapida_observacion',
            field=models.CharField(max_length=200, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='nitritos_observacion',
            field=models.CharField(max_length=200, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='pap_observacion',
            field=models.CharField(max_length=200, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='rapida_sifilis_2_observacion',
            field=models.CharField(max_length=200, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='rapida_sifilis_observacion',
            field=models.CharField(max_length=200, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='rapida_vih_1_observacion',
            field=models.CharField(max_length=200, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='rapida_vih_2_observacion',
            field=models.CharField(max_length=200, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='tamizaje_hepatitis_b_observacion',
            field=models.CharField(max_length=200, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='tolerancia_glucosa_observacion',
            field=models.CharField(max_length=200, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='torch_observacion',
            field=models.CharField(max_length=200, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='tpha_observacion',
            field=models.CharField(max_length=200, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='urocultivo_observacion',
            field=models.CharField(max_length=200, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='vdrl_rp_1_observacion',
            field=models.CharField(max_length=200, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='vdrl_rp_2_observacion',
            field=models.CharField(max_length=200, verbose_name='Observaci\xf3n', blank=True),
            preserve_default=True,
        ),
    ]
