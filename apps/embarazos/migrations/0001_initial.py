# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bebe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('terminacion', models.CharField(default=b'vaginal', max_length=20, verbose_name='Terminacion', choices=[(b'vaginal', 'Parto Vaginal'), (b'cesarea', 'Cesarea'), (b'aborto', 'Aborto'), (b'aborto molar', 'Aborto Molar'), (b'obito', 'Obito'), (b'ectopico', 'Ect\xf3pico'), (b'no aplica', 'No aplica')])),
                ('vive', models.BooleanField(default=True)),
                ('muerte', models.CharField(default=b'no aplica', max_length=20, choices=[(b'no aplica', 'No aplica'), (b'nacio muerto', 'Nacio muerto'), (b'menor primera semana', '< 1ra semana'), (b'mayor primera semana', '> 1ra semana')])),
                ('sexo', models.CharField(default=b'', max_length=1, null=True, blank=True, choices=[(b'M', 'Masculino'), (b'F', 'Femenino'), (b'', b'--')])),
                ('lactancia', models.CharField(default=b'no aplica', max_length=20, verbose_name='Lactancia', choices=[(b'no hubo', 'No hubo'), (b'menos 6 meses', 'Menos de 6 meses'), (b'mas 6 meses', '6 meses a mas'), (b'no aplica', 'No aplica')])),
                ('fecha', models.DateField()),
                ('peso', models.IntegerField(default=0, null=True)),
                ('aborto', models.CharField(default=b'no aplica', max_length=20, null=True, verbose_name='Aborto', choices=[(b'no aplica', 'No aplica'), (b'completo', 'Completo'), (b'incompleto', 'Incompleto'), (b'septico', 'S\xe9ptico'), (b'frusto retenido', 'Frusto retenido')])),
                ('edad_gestacional', models.SmallIntegerField(default=0)),
                ('lugar', models.CharField(default=b'hospitalario', max_length=20, verbose_name='Lugar', choices=[(b'hospitalario', 'Hospitalario'), (b'domiciliario', 'Domiciliario')])),
                ('observacion', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ecografia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.IntegerField(default=1, verbose_name='Numero')),
                ('eg_semana', models.SmallIntegerField(default=0, verbose_name='EG Semana', choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40), (41, 41), (42, 42)])),
                ('eg_dia', models.SmallIntegerField(default=0, verbose_name='EG Dia', choices=[(0, b'0/7'), (1, b'1/7'), (2, b'2/7'), (3, b'3/7'), (4, b'4/7'), (5, b'5/7'), (6, b'6/7')])),
                ('fecha', models.DateField(verbose_name='Fecha de la ecograf\xeda')),
                ('edad_gestacional_actual', models.CharField(max_length=20, null=True, verbose_name='Edad gestacional actual', blank=True)),
                ('fecha_probable_parto', models.DateField(null=True, blank=True)),
                ('lugar', models.CharField(max_length=255, null=True, verbose_name=b'Lugar', blank=True)),
                ('observacion', models.TextField(default=b'', verbose_name='Observacion', blank=True)),
                ('longitud_cefalo_caudal', models.SmallIntegerField(null=True, verbose_name=b'Longitud Cefalo Caudal', blank=True)),
                ('diametro_biparietal', models.SmallIntegerField(null=True, verbose_name=b'Diametro Biparietal', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Ecografia',
                'verbose_name_plural': 'Ecografias',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Embarazo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('padre', models.CharField(max_length=100, null=True, verbose_name='Nombre del padre', blank=True)),
                ('fum', models.DateField(null=True, verbose_name='FUM', blank=True)),
                ('fum_confiable', models.NullBooleanField(default=None, verbose_name='\xbfFUM es confiable?')),
                ('fecha_probable_parto_ultima_menstruacion', models.DateField(null=True, verbose_name='Fecha Probable FUM', blank=True)),
                ('talla', models.IntegerField(verbose_name='Talla')),
                ('peso', models.FloatField(verbose_name='Peso habitual antes del embarazo', validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(200)])),
                ('imc', models.FloatField(default=0, verbose_name='IMC')),
                ('imc_clasificacion', models.CharField(max_length=20, null=True, verbose_name=b'IMC clasificacion', blank=True)),
                ('violencia_familiar', models.NullBooleanField(verbose_name='Violencia Familiar')),
                ('perdida_interes_placer', models.NullBooleanField()),
                ('triste_deprimida_sin_esperanza', models.NullBooleanField()),
                ('usa_drogas', models.NullBooleanField(verbose_name='Usa drogas')),
                ('numero_cigarros_diarios', models.SmallIntegerField(default=0, verbose_name='Numero de cigarros')),
                ('captada', models.NullBooleanField(default=None, verbose_name='\xbfCaptada?')),
                ('referida', models.NullBooleanField(default=None)),
                ('hospitalizacion', models.NullBooleanField(default=None, verbose_name='Hospitalizacion')),
                ('hospitalizacion_fecha', models.DateField(null=True, verbose_name='Fecha', blank=True)),
                ('emergencia', models.NullBooleanField(default=None, verbose_name='Emergencia')),
                ('emergencia_fecha', models.DateField(null=True, verbose_name='Fecha', blank=True)),
                ('activo', models.NullBooleanField(default=False, verbose_name='Activo')),
                ('chart_ganancia_peso_materno', models.ImageField(null=True, upload_to=b'charts', blank=True)),
                ('chart_altura_uterina', models.ImageField(null=True, upload_to=b'charts', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Embarazo',
                'verbose_name_plural': 'Embarazos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FichaProblema',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('poco_interes_o_placer', models.CharField(default=b'nunca', max_length=50, choices=[(b'nunca', b'Nunca'), (b'varios dias', b'Varios dias'), (b'mas de la mitad de los dias', b'Mas de las mitad de los dias'), (b'casi todos los dias', b'Casi todos los dias')])),
                ('desanimada_deprimida', models.CharField(default=b'nunca', max_length=50, choices=[(b'nunca', b'Nunca'), (b'varios dias', b'Varios dias'), (b'mas de la mitad de los dias', b'Mas de las mitad de los dias'), (b'casi todos los dias', b'Casi todos los dias')])),
                ('problemas_dormir', models.CharField(default=b'nunca', max_length=50, choices=[(b'nunca', b'Nunca'), (b'varios dias', b'Varios dias'), (b'mas de la mitad de los dias', b'Mas de las mitad de los dias'), (b'casi todos los dias', b'Casi todos los dias')])),
                ('cansancio', models.CharField(default=b'nunca', max_length=50, choices=[(b'nunca', b'Nunca'), (b'varios dias', b'Varios dias'), (b'mas de la mitad de los dias', b'Mas de las mitad de los dias'), (b'casi todos los dias', b'Casi todos los dias')])),
                ('alimenticio', models.CharField(default=b'nunca', max_length=50, choices=[(b'nunca', b'Nunca'), (b'varios dias', b'Varios dias'), (b'mas de la mitad de los dias', b'Mas de las mitad de los dias'), (b'casi todos los dias', b'Casi todos los dias')])),
                ('falta_autoestima', models.CharField(default=b'nunca', max_length=50, choices=[(b'nunca', b'Nunca'), (b'varios dias', b'Varios dias'), (b'mas de la mitad de los dias', b'Mas de las mitad de los dias'), (b'casi todos los dias', b'Casi todos los dias')])),
                ('dificultad_concentracion', models.CharField(default=b'nunca', max_length=50, choices=[(b'nunca', b'Nunca'), (b'varios dias', b'Varios dias'), (b'mas de la mitad de los dias', b'Mas de las mitad de los dias'), (b'casi todos los dias', b'Casi todos los dias')])),
                ('mueve_lento_o_hiperactivo', models.CharField(default=b'nunca', max_length=50, choices=[(b'nunca', b'Nunca'), (b'varios dias', b'Varios dias'), (b'mas de la mitad de los dias', b'Mas de las mitad de los dias'), (b'casi todos los dias', b'Casi todos los dias')])),
                ('pensamientos_autodestructivos', models.CharField(default=b'nunca', max_length=50, choices=[(b'nunca', b'Nunca'), (b'varios dias', b'Varios dias'), (b'mas de la mitad de los dias', b'Mas de las mitad de los dias'), (b'casi todos los dias', b'Casi todos los dias')])),
                ('difucultad_cumplir_labores', models.CharField(default=b'nada en absoluto', max_length=50, choices=[(b'nada en absoluto', b'Nada en absoluto'), (b'algo dificil', b'Algo dificil'), (b'muy dificil', b'Muy dificil'), (b'extremadamente dificil', b'Extremadamente dificil')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FichaViolenciaFamiliar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('agresores', models.TextField(null=True, verbose_name='Agresor(es)', blank=True)),
                ('hematomas', models.NullBooleanField(default=None, verbose_name='Hematomas, contusiones inexplicables')),
                ('cicatrices', models.NullBooleanField(default=None, verbose_name='Cicatrices, quemaduras')),
                ('fracturas', models.NullBooleanField(default=None, verbose_name='Fracturas inexplicables')),
                ('mordeduras', models.NullBooleanField(default=None, verbose_name='Marca de moderduras')),
                ('lesiones', models.NullBooleanField(default=None, verbose_name='Lesiones de vulva, perineo, recto, etc')),
                ('laceraciones', models.NullBooleanField(default=None, verbose_name='Laceraciones en boca, mejillas, ojos, etc')),
                ('quejas_cronicas', models.NullBooleanField(default=None, verbose_name='Quejas cr\xf3nicas sin causa f\xedsica: cefalea problemas de sue\xf1o (mucho sue\xf1o, interrupci\xf3n del sue\xf1o)')),
                ('problemas_apetito', models.NullBooleanField(default=None, verbose_name='Problemas con apetito')),
                ('enuresis', models.NullBooleanField(default=None, verbose_name='Enuresis (ni\xf1os)')),
                ('falta_de_confianza', models.NullBooleanField(default=None, verbose_name='Extrema falta de confianza en s\xed mismo')),
                ('tristeza', models.NullBooleanField(default=None, verbose_name='Tristeza, depresi\xf3n o angustia')),
                ('retraimiento', models.NullBooleanField(default=None, verbose_name='Retraimiento')),
                ('llanto_frecuente', models.NullBooleanField(default=None, verbose_name='Llanto frecuente')),
                ('necesidad_de_ganar', models.NullBooleanField(default=None, verbose_name='Exagerada necesidad de ganar, sobresalir')),
                ('demanda_de_atencion', models.NullBooleanField(default=None, verbose_name='Demandas excesivas de atenci\xf3n')),
                ('agresividad_pasividad', models.NullBooleanField(default=None, verbose_name='Mucha agresividad o pasividad frente a otros ni\xf1os')),
                ('tartamudeo', models.NullBooleanField(default=None, verbose_name='Tartamudeo')),
                ('temor_padres_hogar', models.NullBooleanField(default=None, verbose_name='Temor a los padres o de llegar al hogar')),
                ('robo_mentira', models.NullBooleanField(default=None, verbose_name='Robo, mentira, fuga, desobediencia, agresividad')),
                ('ausentismo_escolar', models.NullBooleanField(default=None, verbose_name='Ausentismo escolar')),
                ('llegar_temprano_salir_tarde_escuela', models.NullBooleanField(default=None, verbose_name='Llegar temprano a la esceula o retirarse tarde')),
                ('bajo_rendimiento_academico', models.NullBooleanField(default=None, verbose_name='Bajo rendimiento acad\xe9mico')),
                ('aislamiento_de_personas', models.NullBooleanField(default=None, verbose_name='Aslamiento de personas')),
                ('intento_suicidio', models.NullBooleanField(default=None, verbose_name='Intento de suicidio')),
                ('usa_drogas_alcohol', models.NullBooleanField(default=None, verbose_name='Uso alcohol, drogas, tranquilizantes o analg\xe9sicos')),
                ('conducta_sexual_inapropiada', models.NullBooleanField(default=None, verbose_name='Conocimiento y conducta sexual inapropiadas (ni\xf1os)')),
                ('irritacion_dolor', models.NullBooleanField(default=None, verbose_name='Irritaci\xf3n, dolor, lesi\xf3n y hemorragia en zona genital')),
                ('embarazo_precoz', models.NullBooleanField(default=None, verbose_name='Embarazo precoz')),
                ('aborto_amenaza_ets', models.NullBooleanField(default=None, verbose_name='Abortos o amenaza de enfermedades de transmisi\xf3n sexual')),
                ('desnutricion', models.NullBooleanField(default=None, verbose_name='Falta de peso o pobre patr\xf3n de crecimiento')),
                ('no_vacunas', models.NullBooleanField(default=None, verbose_name='No vacunas o atenci\xf3n de salud')),
                ('accidentes_enfermedades_frecuentes', models.NullBooleanField(default=None, verbose_name='Accidentes o enfermedades muy frecuentes')),
                ('descuido_higiene', models.NullBooleanField(default=None, verbose_name='Descuido en higiene y ali\xf1o')),
                ('falta_estimulacion_desarrollo', models.NullBooleanField(default=None, verbose_name='Falta de estimulaci\xf3n del desarrollo')),
                ('fatiga', models.NullBooleanField(default=None, verbose_name='Fatiga, sue\xf1o, hambre')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Ficha violencia familiar',
                'verbose_name_plural': 'Fichas de violencia familiar',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlanParto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('acompaniante_nombre_1', models.CharField(max_length=200, blank=True)),
                ('acompaniante_parentesco_1', models.CharField(max_length=50, blank=True)),
                ('acompaniante_telefono_1', models.CharField(blank=True, max_length=20, validators=[django.core.validators.RegexValidator(regex=b'^[0-9]+$', message='Solo se permiten n\xfameros')])),
                ('acompaniante_dni_1', models.CharField(blank=True, max_length=b'8', validators=[django.core.validators.RegexValidator(regex=b'[0-9]{8}$', message='El DNI debe tener 8 digitos')])),
                ('acompaniante_nombre_2', models.CharField(max_length=200, blank=True)),
                ('acompaniante_parentesco_2', models.CharField(max_length=50, blank=True)),
                ('acompaniante_telefono_2', models.CharField(blank=True, max_length=20, validators=[django.core.validators.RegexValidator(regex=b'^[0-9]+$', message='Solo se permiten n\xfameros')])),
                ('acompaniante_dni_2', models.CharField(blank=True, max_length=b'8', validators=[django.core.validators.RegexValidator(regex=b'[0-9]{8}$', message='El DNI debe tener 8 digitos')])),
                ('acompaniante_nombre_3', models.CharField(max_length=200, blank=True)),
                ('acompaniante_parentesco_3', models.CharField(max_length=50, blank=True)),
                ('acompaniante_telefono_3', models.CharField(blank=True, max_length=20, validators=[django.core.validators.RegexValidator(regex=b'^[0-9]+$', message='Solo se permiten n\xfameros')])),
                ('acompaniante_dni_3', models.CharField(blank=True, max_length=b'8', validators=[django.core.validators.RegexValidator(regex=b'[0-9]{8}$', message='El DNI debe tener 8 digitos')])),
                ('donador_nombre_1', models.CharField(max_length=200, blank=True)),
                ('donador_telefono_1', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(regex=b'^[0-9]+$', message='Solo se permiten n\xfameros')])),
                ('donador_nombre_2', models.CharField(max_length=200, blank=True)),
                ('donador_telefono_2', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(regex=b'^[0-9]+$', message='Solo se permiten n\xfameros')])),
                ('e1_edad_gestacional', models.CharField(max_length=10, null=True, blank=True)),
                ('e1_fecha', models.DateField(null=True, blank=True)),
                ('e1_lugar_atencion', models.CharField(blank=True, max_length=20, choices=[(b'hospital', b'Hospital'), (b'centro salud', b'Centro de salud'), (b'posta salud', b'Posta de salud'), (b'domicilio', b'Domicilio'), (b'otros', b'Otros')])),
                ('e1_lugar_atencion_otros', models.CharField(max_length=200, null=True, blank=True)),
                ('e1_persona_que_atendera_parto', models.CharField(max_length=200, blank=True)),
                ('e1_posicion_parto', models.CharField(blank=True, max_length=20, choices=[(b'echada', b'Echada'), (b'cuclillas', b'Cuclillas'), (b'dorso lateral', b'Dorso Lateral'), (b'otros', b'Otros')])),
                ('e1_posicion_parto_otros', models.CharField(max_length=200, null=True, blank=True)),
                ('e1_transporte', models.CharField(blank=True, max_length=20, choices=[(b'carro', b'Carro'), (b'acemila', b'Acemila'), (b'camilla', b'Camilla'), (b'otros', b'Otros')])),
                ('e1_transporte_otros', models.CharField(max_length=200, null=True, blank=True)),
                ('e1_tiempo_llegada', models.SmallIntegerField(null=True, verbose_name='Tiempo de llegada', blank=True)),
                ('e1_persona_que_avisara_centro_salud', models.CharField(max_length=200, null=True, blank=True)),
                ('e1_persona_que_cuidara_casa', models.CharField(max_length=200, null=True, blank=True)),
                ('e1_ira_casa_espera', models.NullBooleanField(default=None)),
                ('e1_sabe_cuando_ira_casa_espera', models.NullBooleanField(default=None)),
                ('e1_sabe_cuando_ira_casa_espera_fecha', models.DateField(null=True, blank=True)),
                ('e2_edad_gestacional', models.CharField(max_length=10, null=True, blank=True)),
                ('e2_fecha', models.DateField(null=True, blank=True)),
                ('e2_lugar_atencion', models.CharField(blank=True, max_length=20, choices=[(b'hospital', b'Hospital'), (b'centro salud', b'Centro de salud'), (b'posta salud', b'Posta de salud'), (b'domicilio', b'Domicilio'), (b'otros', b'Otros')])),
                ('e2_lugar_atencion_otros', models.CharField(max_length=200, null=True, blank=True)),
                ('e2_persona_que_atendera_parto', models.CharField(max_length=200, blank=True)),
                ('e2_posicion_parto', models.CharField(blank=True, max_length=20, choices=[(b'echada', b'Echada'), (b'cuclillas', b'Cuclillas'), (b'dorso lateral', b'Dorso Lateral'), (b'otros', b'Otros')])),
                ('e2_posicion_parto_otros', models.CharField(max_length=200, null=True, blank=True)),
                ('e2_transporte', models.CharField(blank=True, max_length=20, choices=[(b'carro', b'Carro'), (b'acemila', b'Acemila'), (b'camilla', b'Camilla'), (b'otros', b'Otros')])),
                ('e2_transporte_otros', models.CharField(max_length=200, null=True, blank=True)),
                ('e2_tiempo_llegada', models.SmallIntegerField(null=True, verbose_name='Tiempo de llegada', blank=True)),
                ('e2_persona_que_avisara_centro_salud', models.CharField(max_length=200, null=True, blank=True)),
                ('e2_persona_que_cuidara_casa', models.CharField(max_length=200, null=True, blank=True)),
                ('e2_ira_casa_espera', models.NullBooleanField(default=None)),
                ('e2_sabe_cuando_ira_casa_espera', models.NullBooleanField(default=None)),
                ('e2_sabe_cuando_ira_casa_espera_fecha', models.DateField(null=True, blank=True)),
                ('e3_edad_gestacional', models.CharField(max_length=10, null=True, blank=True)),
                ('e3_fecha', models.DateField(null=True, blank=True)),
                ('e3_lugar_atencion', models.CharField(blank=True, max_length=20, choices=[(b'hospital', b'Hospital'), (b'centro salud', b'Centro de salud'), (b'posta salud', b'Posta de salud'), (b'domicilio', b'Domicilio'), (b'otros', b'Otros')])),
                ('e3_lugar_atencion_otros', models.CharField(max_length=200, null=True, blank=True)),
                ('e3_persona_que_atendera_parto', models.CharField(max_length=200, blank=True)),
                ('e3_posicion_parto', models.CharField(blank=True, max_length=20, choices=[(b'echada', b'Echada'), (b'cuclillas', b'Cuclillas'), (b'dorso lateral', b'Dorso Lateral'), (b'otros', b'Otros')])),
                ('e3_posicion_parto_otros', models.CharField(max_length=200, null=True, blank=True)),
                ('e3_transporte', models.CharField(blank=True, max_length=20, choices=[(b'carro', b'Carro'), (b'acemila', b'Acemila'), (b'camilla', b'Camilla'), (b'otros', b'Otros')])),
                ('e3_transporte_otros', models.CharField(max_length=200, null=True, blank=True)),
                ('e3_tiempo_llegada', models.SmallIntegerField(null=True, verbose_name='Tiempo de llegada', blank=True)),
                ('e3_persona_que_avisara_centro_salud', models.CharField(max_length=200, null=True, blank=True)),
                ('e3_persona_que_cuidara_casa', models.CharField(max_length=200, null=True, blank=True)),
                ('e3_ira_casa_espera', models.NullBooleanField(default=None)),
                ('e3_sabe_cuando_ira_casa_espera', models.NullBooleanField(default=None)),
                ('e3_sabe_cuando_ira_casa_espera_fecha', models.DateField(null=True, blank=True)),
                ('observaciones', models.TextField(verbose_name=b'Observaciones', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UltimoEmbarazo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.PositiveSmallIntegerField(default=1)),
                ('tipo', models.CharField(default=b'unico', max_length=10, choices=[(b'unico', 'Unico'), (b'multiple', 'Multiple')])),
                ('wawared', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Ultimo embarazo',
                'verbose_name_plural': 'Ultimos embarazos',
            },
            bases=(models.Model,),
        ),
    ]