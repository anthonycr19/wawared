# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('embarazos', '0003_auto_20141205_1039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planparto',
            name='acompaniante_dni_1',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='acompaniante_dni_2',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='acompaniante_dni_3',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='acompaniante_nombre_1',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='acompaniante_nombre_2',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='acompaniante_nombre_3',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='acompaniante_parentesco_1',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='acompaniante_parentesco_2',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='acompaniante_parentesco_3',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='acompaniante_telefono_1',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='acompaniante_telefono_2',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='acompaniante_telefono_3',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='donador_nombre_1',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='donador_nombre_2',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='donador_telefono_1',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='donador_telefono_2',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e1_ira_casa_espera',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e1_persona_que_atendera_parto',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e1_persona_que_avisara_centro_salud',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e1_persona_que_cuidara_casa',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e1_posicion_parto',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e1_posicion_parto_otros',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e1_sabe_cuando_ira_casa_espera',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e1_sabe_cuando_ira_casa_espera_fecha',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e1_tiempo_llegada',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e1_transporte',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e1_transporte_otros',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e2_ira_casa_espera',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e2_persona_que_atendera_parto',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e2_persona_que_avisara_centro_salud',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e2_persona_que_cuidara_casa',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e2_sabe_cuando_ira_casa_espera',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e2_sabe_cuando_ira_casa_espera_fecha',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e2_tiempo_llegada',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e3_edad_gestacional',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e3_fecha',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e3_ira_casa_espera',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e3_lugar_atencion',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e3_lugar_atencion_otros',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e3_persona_que_atendera_parto',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e3_persona_que_avisara_centro_salud',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e3_persona_que_cuidara_casa',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e3_posicion_parto',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e3_posicion_parto_otros',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e3_sabe_cuando_ira_casa_espera',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e3_sabe_cuando_ira_casa_espera_fecha',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e3_tiempo_llegada',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e3_transporte',
        ),
        migrations.RemoveField(
            model_name='planparto',
            name='e3_transporte_otros',
        ),
        migrations.AddField(
            model_name='planparto',
            name='donador_1_domicilio',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='donador_1_edad',
            field=models.CharField(blank=True, max_length=2, null=True, validators=[django.core.validators.RegexValidator(regex=b'[0-9]{2}$', message='La edad solo debe contener d\xedgitos')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='donador_1_nombre',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='donador_1_parentesco',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='donador_1_tipo_sangre',
            field=models.CharField(max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='donador_2_domicilio',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='donador_2_edad',
            field=models.CharField(blank=True, max_length=2, null=True, validators=[django.core.validators.RegexValidator(regex=b'[0-9]{2}$', message='La edad solo debe contener d\xedgitos')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='donador_2_nombre',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='donador_2_parentesco',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='donador_2_tipo_sangre',
            field=models.CharField(max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='e1_distancia_tiempo_llegada',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='e1_fecha_observacion',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='e1_fecha_probable_parto',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='e1_fecha_probable_parto_observacion',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='e1_lugar_atencion_observacion',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='e1_lugar_atencion_razon_eleccion',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='e1_se_quedara_todo_el_embarazo_en_domicilio_actual',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='e2_persona_cuidara_hijos_en_casa',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='e2_persona_cuidara_hijos_en_casa_observacion',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='e2_persona_que_acompania_en_el_parto',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='e2_persona_que_acompania_en_el_parto_observacion',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='e2_posicion_parto_observacion',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='e2_tiempo_llegada_1',
            field=models.SmallIntegerField(null=True, verbose_name='Tiempo de llegada opci\xf3n 1', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='e2_tiempo_llegada_1_observacion',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='e2_tiempo_llegada_2',
            field=models.SmallIntegerField(null=True, verbose_name='Tiempo de llegada opci\xf3n 2', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='e2_tiempo_llegada_2_observacion',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planparto',
            name='e2_transporte_observacion',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='planparto',
            name='e1_fecha',
            field=models.DateField(null=True, verbose_name=b'Fecha', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='planparto',
            name='e1_lugar_atencion',
            field=models.CharField(blank=True, max_length=20, choices=[(b'hospital', b'Hospital'), (b'centro salud', b'Centro de salud'), (b'posta salud', b'Posta de salud'), (b'domicilio', b'Domicilio'), (b'no ha decidido', b'No ha decidido'), (b'otros', b'Otros')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='planparto',
            name='e2_lugar_atencion',
            field=models.CharField(blank=True, max_length=20, choices=[(b'hospital', b'Hospital'), (b'centro salud', b'Centro de salud'), (b'posta salud', b'Posta de salud'), (b'domicilio', b'Domicilio'), (b'no ha decidido', b'No ha decidido'), (b'otros', b'Otros')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='planparto',
            name='e2_posicion_parto',
            field=models.CharField(blank=True, max_length=20, choices=[(b'echada', b'Echada'), (b'cuclillas', b'Cuclillas'), (b'parada', b'Parada'), (b'otros', b'Otros')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='planparto',
            name='e2_transporte',
            field=models.CharField(blank=True, max_length=20, choices=[(b'tazi', b'Taxi'), (b'motitaxi', b'Mototaxi'), (b'micro', b'Micro'), (b'otros', b'Otros')]),
            preserve_default=True,
        ),
    ]
