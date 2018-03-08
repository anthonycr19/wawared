# -*- coding: utf-8 -*-
from io import BytesIO
import csv
import datetime
import os

import matplotlib
matplotlib.use('Agg')  # NOQA
# usado para evitar error el momento de usar la libreria
import matplotlib.pyplot as plt
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.db.models import Q

from common.util import print_choices
from controles import Control

ZERO_TO_3_CHOICES = tuple(((str(i), str(i)) for i in range(4)))


def ganancia_peso_materno_data_segun_imc(imc, multiple=False):
    if imc < 18.5:
        key_prefix = 'BAJO_PESO'
    elif 18.5 <= imc < 25.0:
        key_prefix = 'NORMAL'
    elif 25.0 <= imc < 30.0:
        key_prefix = 'SOBREPESO'
    else:
        key_prefix = 'OBESIDAD'
    if key_prefix == 'BAJO_PESO':
        min_key, max_key = '_MIN', '_MAX'
    else:
        if multiple:
            min_key, max_key = '_MELLIZOS_MIN', '_MELLIZOS_MAX'
        else:
            min_key, max_key = '_UNICO_MIN', '_UNICO_MAX'
    path = os.path.join(settings.BASE_DIR, 'data', 'ganancia_peso_materno.csv')
    res = []
    with open(path) as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            # Cuando no se encuentre data(mellizos) se considera valor 0
            res.append({
                'min': float(row[key_prefix + min_key] or 0),
                'max': float(row[key_prefix + max_key] or 0),
                'semana': int(row['SEMANA']),
            })
    return res


class Embarazo(models.Model):
    paciente = models.ForeignKey(
        'pacientes.Paciente', related_name='embarazos')
    establecimiento = models.ForeignKey(
        'establecimientos.Establecimiento', related_name='embarazos')

    padre = models.CharField(
        u'Nombre del padre', max_length=100, null=True, blank=True)
    padre_apellido_paterno = models.CharField(
        'Apellido paterno del padre', max_length=50, null=True, blank=True)
    padre_apellido_materno = models.CharField(
        'Apellido materno del padre', max_length=50, null=True, blank=True)
    padre_nombres = models.CharField(
        'Nombres del padre', max_length=50, null=True, blank=True)

    # Fecha ultima menstruacion
    fum = models.DateField(u'FUM', null=True, blank=True)
    fum_confiable = models.NullBooleanField(
        u'¿FUM es confiable?', default=None)
    fecha_probable_parto_ultima_menstruacion = models.DateField(
        u'Fecha Probable FUM', null=True, blank=True)
    talla = models.FloatField(u'Talla')
    peso = models.FloatField(u'Peso habitual antes del embarazo', validators=[
        MinValueValidator(10), MaxValueValidator(200)
    ])
    imc = models.FloatField(u'IMC', default=0)
    imc_clasificacion = models.CharField(
        'IMC clasificacion', max_length=20, blank=True, null=True)

    # Ficha problemas
    perdida_interes_placer = models.CharField(
        max_length=5, blank=True, null=True, choices=ZERO_TO_3_CHOICES)
    triste_deprimida_sin_esperanza = models.CharField(
        max_length=5, blank=True, null=True, choices=ZERO_TO_3_CHOICES)
    depresion_puntaje = models.SmallIntegerField(
        'Puntaje', default=None, null=True, blank=True)
    fecha_tamizaje = models.DateField(
        'Fecha de tamizaje', null=True, blank=True)

    usa_drogas = models.NullBooleanField(u'Usa drogas')
    numero_cigarros_diarios = models.IntegerField(
        u'Numero de cigarros', default=0, validators=[MinValueValidator(0), MaxValueValidator(200)])

    # Ingreso
    captada = models.NullBooleanField(u'¿Captada?', default=None)
    referida = models.NullBooleanField(default=None)
    # Hospitalizacion
    hospitalizacion = models.NullBooleanField(
        u'Hospitalizacion', blank=True, default=None)
    hospitalizacion_fecha = models.DateField(u'Fecha', blank=True, null=True)
    hospitalizacion_diagnosticos = models.ManyToManyField(
        'cie.ICD10Base', related_name='embarazos_hospitalizacion', null=True,
        blank=True)
    # Emergencia
    emergencia = models.NullBooleanField(
        u'Emergencia', blank=True, default=None)
    emergencia_fecha = models.DateField(u'Fecha', blank=True, null=True)
    emergencia_diagnosticos = models.ManyToManyField(
        'cie.ICD10Base', related_name='embarazos_emergencias', null=True,
        blank=True)

    activo = models.NullBooleanField(u'Activo', default=False, blank=True)

    chart_ganancia_peso_materno = models.ImageField(
        upload_to='charts', blank=True, null=True)
    chart_altura_uterina = models.ImageField(
        upload_to='charts', blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)

    class Meta:
        verbose_name = u'Embarazo'
        verbose_name_plural = u'Embarazos'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.imc_clasificacion = self.get_imc_clasificacion()
        super(Embarazo, self).save(force_insert, force_update, using, update_fields)

    def get_imc_clasificacion(self):
        if self.imc < 19.8:
            return 'bajo peso'
        elif 19.8 <= self.imc <= 26:
            return 'normal'
        elif 26 < self.imc <= 29:
            return 'sobrepeso'
        else:
            return 'obesidad'

    def __unicode__(self):
        return self.paciente.nombre_completo

    @property
    def numero_controles(self):
        return self.controles.count()

    @property
    def primera_ecografia(self):
        return self.ecografias.all().order_by('fecha').first()

    altura_uterina_percentiles = [
        {'10': 8.0, '15': 8.0, '50': 10.8, '75': 11.0, 'semana': 13, '90': 12.0},
        {'10': 8.5, '15': 10.0, '50': 11.0, '75': 13.0, 'semana': 14, '90': 14.5},
        {'10': 9.5, '15': 10.5, '50': 12.5, '75': 14.0, 'semana': 15, '90': 15.0},
        {'10': 11.5, '15': 12.5, '50': 14.0, '75': 16.0, 'semana': 16, '90': 18.0},
        {'10': 12.5, '15': 13.0, '50': 15.0, '75': 17.5, 'semana': 17, '90': 18.0},
        {'10': 13.5, '15': 15.0, '50': 16.5, '75': 18.0, 'semana': 18, '90': 19.0},
        {'10': 14.0, '15': 16.0, '50': 17.5, '75': 19.0, 'semana': 19, '90': 19.5},
        {'10': 15.0, '15': 17.0, '50': 18.0, '75': 19.5, 'semana': 20, '90': 21.0},
        {'10': 15.5, '15': 18.5, '50': 19.0, '75': 20.0, 'semana': 21, '90': 21.5},
        {'10': 16.5, '15': 18.5, '50': 20.0, '75': 21.5, 'semana': 22, '90': 22.5},
        {'10': 17.5, '15': 19.5, '50': 21.0, '75': 22.5, 'semana': 23, '90': 23.0},
        {'10': 18.5, '15': 20.5, '50': 22.0, '75': 23.0, 'semana': 24, '90': 24.0},
        {'10': 19.5, '15': 21.0, '50': 22.5, '75': 24.0, 'semana': 25, '90': 25.5},
        {'10': 20.0, '15': 21.5, '50': 23.0, '75': 24.5, 'semana': 26, '90': 25.5},
        {'10': 20.5, '15': 21.5, '50': 23.5, '75': 25.0, 'semana': 27, '90': 26.5},
        {'10': 21.0, '15': 23.0, '50': 25.0, '75': 26.0, 'semana': 28, '90': 27.0},
        {'10': 22.4, '15': 24.0, '50': 25.5, '75': 26.5, 'semana': 29, '90': 28.0},
        {'10': 23.5, '15': 24.5, '50': 26.5, '75': 28.0, 'semana': 30, '90': 29.0},
        {'10': 24.0, '15': 26.0, '50': 27.0, '75': 28.0, 'semana': 31, '90': 29.5},
        {'10': 25.0, '15': 26.5, '50': 28.0, '75': 29.5, 'semana': 32, '90': 30.0},
        {'10': 25.5, '15': 26.5, '50': 29.0, '75': 30.0, 'semana': 33, '90': 31.0},
        {'10': 26.0, '15': 27.5, '50': 29.5, '75': 31.0, 'semana': 34, '90': 32.0},
        {'10': 26.5, '15': 28.5, '50': 30.5, '75': 32.0, 'semana': 35, '90': 33.0},
        {'10': 28.0, '15': 29.0, '50': 31.0, '75': 32.5, 'semana': 36, '90': 33.0},
        {'10': 28.5, '15': 29.5, '50': 31.5, '75': 33.0, 'semana': 37, '90': 34.0},
        {'10': 29.5, '15': 30.5, '50': 33.0, '75': 33.5, 'semana': 38, '90': 34.0},
        {'10': 30.5, '15': 31.0, '50': 33.5, '75': 33.5, 'semana': 39, '90': 34.0},
        {'10': 31.0, '15': 31.0, '50': 33.5, '75': 33.5, 'semana': 40, '90': 34.5}]

    def create_incremento_peso_materno_chart(self):
        from controles.models import ExamenFisicoFetal
        # local import to avoid circular import error

        ultimo_control = self.controles.order_by('-atencion_fecha').first()
        if ultimo_control is not None and ExamenFisicoFetal.objects.filter(control=ultimo_control).count() > 1:
            multiple = True
        else:
            multiple = False

        if ultimo_control is None:
            imc = ultimo_control.imc
            imc_clasificacion = ultimo_control.imc_clasificacion
        else:
            imc = self.imc
            imc_clasificacion = self.imc_clasificacion

        valores = ganancia_peso_materno_data_segun_imc(imc, multiple=multiple)

        p_25_x = []
        p_25_y = []
        p_90_x = []
        p_90_y = []
        for per in valores:
            p_25_x.append(per['semana'])
            p_25_y.append(per['min'])
            p_90_x.append(per['semana'])
            p_90_y.append(per['max'])
        controles_x = []
        controles_y = []
        for control in self.controles.all().order_by('numero'):
            if int(control.edad_gestacional_semanas) >= 13:
                diff = float(abs((control.peso - self.peso)))
                controles_x.append(int(control.edad_gestacional_semanas))
                controles_y.append(diff)
        if multiple:
            # para el caso de mellizos solo se considera desde la semana 14
            p_25_x = p_25_x[13:]
            p_25_y = p_25_y[13:]
            p_90_x = p_90_x[13:]
            p_90_y = p_90_y[13:]
        plt.xlabel('SEMANAS DE AMENORREA')
        plt.ylabel('INCREMENTO DE PESO MATERNO')
        plt.plot(p_25_x, p_25_y, 'b')
        plt.plot(p_90_x, p_90_y, 'r')
        plt.plot(controles_x, controles_y, 'g')
        plt.plot(controles_x, controles_y, 'gs')
        plt.text(5, 13, 'IMC: {}'.format(imc_clasificacion.upper()), fontsize=18)
        plt.grid(True)
        io_image = BytesIO()
        plt.savefig(io_image, bbox_inches='tight', transparent="True", pad_inches=0.1)
        self.chart_ganancia_peso_materno.save(
            'ganancia_peso_chart_{}.png'.format(self.id),
            ContentFile(io_image.getvalue()))
        plt.close()
        self.save()

    def create_altura_uterina_chart(self):
        p_10_x = []
        p_10_y = []
        p_90_x = []
        p_90_y = []
        for per in self.altura_uterina_percentiles:
            p_10_x.append(int(per['semana']))
            p_10_y.append(per['10'])
            p_90_x.append(int(per['semana']))
            p_90_y.append(per['90'])
        controles_x = []
        controles_y = []
        for control in self.controles.all().order_by('numero'):
            if int(control.edad_gestacional_semanas) >= 13:
                controles_x.append(int(control.edad_gestacional_semanas))
                controles_y.append(control.altura_uterina)
        plt.xlabel('SEMANAS DE AMENORREA')
        plt.ylabel('ALTURA UTERINA')
        plt.plot(p_10_x, p_10_y, 'b')
        plt.plot(p_90_x, p_90_y, 'r')
        plt.plot(controles_x, controles_y, 'g')
        plt.plot(controles_x, controles_y, 'gs')
        plt.grid(True)
        io_image = BytesIO()
        plt.savefig(io_image, bbox_inches='tight', transparent="True", pad_inches=0.1)
        self.chart_altura_uterina.save(
            'altura_uterina_chart_{}.png'.format(self.id),
            ContentFile(io_image.getvalue()))
        plt.close()
        self.save()

    def semana_actual_probable(self):
        """
        Se calcula a partir de la fecha probable de parto
        """
        if self.fecha_probable_parto_ultima_menstruacion is None:
            return None

        fecha_inicio = self.fecha_probable_parto_ultima_menstruacion
        fecha_inicio -= datetime.timedelta(days=40 * 7)
        return (datetime.date.today() - fecha_inicio).days / 7 + 1


class FichaViolenciaFamiliar(models.Model):
    embarazo = models.OneToOneField(
        'Embarazo', related_name='ficha_violencia_familiar')
    paciente = models.ForeignKey(
        'pacientes.Paciente', related_name='fichas_violencia_familiar')

    violencia_fisica = models.NullBooleanField(default=None)
    violencia_fisica_agresores = models.CharField(
        max_length=100, blank=True, null=True)
    violencia_psicologica = models.NullBooleanField(default=None)
    violencia_psicologica_agresores = models.CharField(
        max_length=100, blank=True, null=True)
    violencia_sexual = models.NullBooleanField(default=None)
    violencia_sexual_agresores = models.CharField(
        max_length=100, blank=True, null=True)

    # Fisicos
    hematomas = models.NullBooleanField(
        u'Hematomas, contusiones inexplicables', default=None, blank=True)
    cicatrices = models.NullBooleanField(
        u'Cicatrices, quemaduras', default=None, blank=True)
    fracturas = models.NullBooleanField(
        u'Fracturas inexplicables', default=None, blank=True)
    mordeduras = models.NullBooleanField(
        u'Marca de moderduras', default=None, blank=True)
    lesiones = models.NullBooleanField(
        u'Lesiones de vulva, perineo, recto, etc', default=None, blank=True)
    laceraciones = models.NullBooleanField(
        u'Laceraciones en boca, mejillas, ojos, etc', default=None, blank=True)
    quejas_cronicas = models.NullBooleanField(
        u'Quejas crónicas sin causa física', default=None, blank=True)
    cefalea = models.NullBooleanField(
        u'Cefalea problemas de sueño (mucho sueño, interrupción del sueño)',
        default=None, blank=True)
    problemas_apetito = models.NullBooleanField(
        u'Problemas con apetito', default=None, blank=True)
    enuresis = models.NullBooleanField(
        u'Enuresis (niños)', default=None, blank=True)

    # Psicologicos
    falta_de_confianza = models.NullBooleanField(
        u'Extrema falta de confianza en sí mismo', default=None, blank=True)
    tristeza = models.NullBooleanField(
        u'Tristeza, depresión o angustia', default=None, blank=True)
    retraimiento = models.NullBooleanField(
        u'Retraimiento', default=None, blank=True)
    llanto_frecuente = models.NullBooleanField(
        u'Llanto frecuente', default=None, blank=True)
    necesidad_de_ganar = models.NullBooleanField(
        u'Exagerada necesidad de ganar, sobresalir', default=None, blank=True)
    demanda_de_atencion = models.NullBooleanField(
        u'Demandas excesivas de atención', default=None, blank=True)
    agresividad_pasividad = models.NullBooleanField(
        u'Mucha agresividad o pasividad frente a otros niños', default=None,
        blank=True)
    tartamudeo = models.NullBooleanField(
        u'Tartamudeo', default=None, blank=True)
    temor_padres_hogar = models.NullBooleanField(
        u'Temor a los padres o de llegar al hogar', default=None, blank=True)
    robo_mentira = models.NullBooleanField(
        u'Robo, mentira, fuga, desobediencia, agresividad', default=None,
        blank=True)
    ausentismo_escolar = models.NullBooleanField(
        u'Ausentismo escolar', default=None, blank=True)
    llegar_temprano_salir_tarde_escuela = models.NullBooleanField(
        u'Llegar temprano a la esceula o retirarse tarde', default=None,
        blank=True)
    bajo_rendimiento_academico = models.NullBooleanField(
        u'Bajo rendimiento académico', default=None, blank=True)
    aislamiento_de_personas = models.NullBooleanField(
        u'Aslamiento de personas', default=None, blank=True)
    intento_suicidio = models.NullBooleanField(
        u'Intento de suicidio', default=None, blank=True)
    usa_drogas_alcohol = models.NullBooleanField(
        u'Uso alcohol, drogas, tranquilizantes o analgésicos', default=None,
        blank=True)

    # Sexuales
    conducta_sexual_inapropiada = models.NullBooleanField(
        u'Conocimiento y conducta sexual inapropiadas (niños)', default=None,
        blank=True)
    irritacion_dolor = models.NullBooleanField(
        u'Irritación, dolor, lesión y hemorragia en zona genital',
        default=None, blank=True)
    embarazo_precoz = models.NullBooleanField(
        u'Embarazo precoz', default=None, blank=True)
    aborto_amenaza_ets = models.NullBooleanField(
        u'Abortos o amenaza de enfermedades de transmisión sexual',
        default=None, blank=True)

    # Negligencia
    desnutricion = models.NullBooleanField(
        u'Falta de peso o pobre patrón de crecimiento', default=None,
        blank=True)
    no_vacunas = models.NullBooleanField(
        u'No vacunas o atención de salud', default=None, blank=True)
    accidentes_enfermedades_frecuentes = models.NullBooleanField(
        u'Accidentes o enfermedades muy frecuentes', default=None, blank=True)
    descuido_higiene = models.NullBooleanField(
        u'Descuido en higiene y aliño', default=None, blank=True)
    falta_estimulacion_desarrollo = models.NullBooleanField(
        u'Falta de estimulación del desarrollo', default=None, blank=True)
    fatiga = models.NullBooleanField(
        u'Fatiga, sueño, hambre', default=None, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)

    class Meta:
        verbose_name = u'Ficha violencia familiar'
        verbose_name_plural = u'Fichas de violencia familiar'


class FichaProblema(models.Model):
    NUNCA = '0'
    VARIOS_DIAS = '1'
    MAS_DE_LA_MITAD_DE_LOS_DIAS = '2'
    CASI_TODOS_LOS_DIAS = '3'

    COMMON_CHOICES = (
        (NUNCA, 'Nunca'),
        (VARIOS_DIAS, 'Varios dias'),
        (MAS_DE_LA_MITAD_DE_LOS_DIAS, 'Mas de las mitad de los dias'),
        (CASI_TODOS_LOS_DIAS, 'Casi todos los dias')
    )

    NADA_EN_ABSOLUTO = 'nada en absoluto'
    ALGO_DIFICIL = 'algo dificil'
    MUY_DIFICIL = 'muy dificil'
    EXTREMADAMENTE_DIFICIL = 'extremadamente dificil'

    CUMPLIR_LABORES_CHOICES = (
        (NADA_EN_ABSOLUTO, 'Nada en absoluto'),
        (ALGO_DIFICIL, 'Algo dificil'),
        (MUY_DIFICIL, 'Muy dificil'),
        (EXTREMADAMENTE_DIFICIL, 'Extremadamente dificil')
    )

    embarazo = models.OneToOneField('Embarazo', related_name='ficha_problema')
    paciente = models.ForeignKey(
        'pacientes.Paciente', related_name='fichas_problema')

    poco_interes_o_placer = models.CharField(
        max_length=50, choices=COMMON_CHOICES, blank=True, null=True)
    desanimada_deprimida = models.CharField(
        max_length=50, choices=COMMON_CHOICES, blank=True, null=True)
    problemas_dormir = models.CharField(
        max_length=50, choices=COMMON_CHOICES, blank=True, null=True)
    cansancio = models.CharField(
        max_length=50, choices=COMMON_CHOICES, blank=True, null=True)
    alimenticio = models.CharField(
        max_length=50, choices=COMMON_CHOICES, blank=True, null=True)
    falta_autoestima = models.CharField(
        max_length=50, choices=COMMON_CHOICES, blank=True, null=True)
    dificultad_concentracion = models.CharField(
        max_length=50, choices=COMMON_CHOICES, blank=True, null=True)
    mueve_lento_o_hiperactivo = models.CharField(
        max_length=50, choices=COMMON_CHOICES, blank=True, null=True)
    pensamientos_autodestructivos = models.CharField(
        max_length=50, choices=COMMON_CHOICES, blank=True, null=True)

    difucultad_cumplir_labores = models.CharField(
        max_length=50, choices=CUMPLIR_LABORES_CHOICES, blank=True, null=True)

    puntaje = models.SmallIntegerField('Puntaje', null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)

    def get_puntaje_cie(self):
        if 4 < self.puntaje <= 9:
            return 'F348'
        elif 9 < self.puntaje <= 14:
            return 'F330'
        elif 14 < self.puntaje <= 19:
            return 'F331'
        elif 20 < self.puntaje:
            return 'F332'
        else:
            return None


class Ecografia(models.Model):
    TIPO_UNICO = 'unico'
    TIPO_MULTIPLE = 'multiple'

    TIPO_EMBARAZO_CHOICES = (
        (TIPO_UNICO, u'Único'),
        (TIPO_MULTIPLE, 'Multiple')
    )

    embarazo = models.ForeignKey('Embarazo', related_name='ecografias')
    establecimiento = models.ForeignKey(
        'establecimientos.Establecimiento', related_name='ecografias')

    numero = models.IntegerField(u'Numero', default=1)
    eg_semana = models.SmallIntegerField(u'EG Semana', choices=(
        (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
        (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15),
        (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22),
        (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29),
        (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36),
        (37, 37), (38, 38), (39, 39), (40, 40), (41, 41), (42, 42)), default=0)
    eg_dia = models.SmallIntegerField(u'EG Dia', choices=(
        (0, '0/7'), (1, '1/7'), (2, '2/7'), (3, '3/7'), (4, '4/7'), (5, '5/7'),
        (6, '6/7'),), default=0)
    fecha = models.DateField(u'Fecha de la ecografía', null=True)
    tipo_embarazo = models.CharField(
        'Tipo de embarazo', max_length=10, choices=TIPO_EMBARAZO_CHOICES,
        default=TIPO_UNICO)
    edad_gestacional_actual = models.CharField(
        u'Edad gestacional actual', max_length=20, blank=True, null=True)
    fecha_probable_parto = models.DateField(blank=True, null=True)
    lugar = models.CharField('Lugar', max_length=255, blank=True, null=True)
    observacion = models.TextField(u'Observacion', blank=True, default='')
    longitud_cefalo_caudal = models.SmallIntegerField(
        'Longitud Cefalo Caudal', blank=True, null=True)
    diametro_biparietal = models.SmallIntegerField(
        'Diametro Biparietal', null=True, blank=True)
    biometria_fetal = models.PositiveSmallIntegerField(u'Biometría Fetal (Perímetro cefálico)', blank=True,
        null=True)
    ila = models.PositiveSmallIntegerField(
        u'Índice de líquido amniótico', blank=True, null=True)
    liquido_amniotico = models.CharField(
        choices=(('n', 'Normal'), ('d', 'Disminuido'), ('a', 'Aumentado'),),
        blank=True, max_length=1)
    microcefalia_fetal = models.CharField(
        choices=(('si', 'Si'), ('no', 'No'),), blank=True, max_length=2,
        verbose_name=u'/'.join([
            u'Informe con probable microcefalia fetal',
            u'calcificación intracraneal']))

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)

    class Meta:
        verbose_name = u'Ecografia'
        verbose_name_plural = u'Ecografias'
        ordering = ('fecha',)

    @property
    def eg_dias(self):
        return self.eg_semana * 7 + self.eg_dia

    def print_eg_dia(self):
        return '{}/7'.format(self.eg_dia)

    @classmethod
    def order_by_date(cls, embarazo):
        counter = 1
        for ecografia in embarazo.ecografias.all().order_by('fecha'):
            ecografia.numero = counter
            ecografia.save()
            counter += 1

    def save(self):
        if self.fecha:
            super(Ecografia, self).save()


class EcografiaDetalle(models.Model):
    ecografia = models.ForeignKey('Ecografia', related_name='ecografia')
    biometria_fetal = models.PositiveSmallIntegerField(
        u'Biometría Fetal (Perímetro cefálico)', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = u'Ecografia Detalle'
        verbose_name_plural = u'Ecografias Detalles'


class UltimoEmbarazo(models.Model):

    """
    Embarazos anteriores de la paciente, se detallan los datos del bebe
    """

    TIPO_UNICO = 'unico'
    TIPO_MULTIPLE = 'multiple'

    TIPO_CHOICES = (
        (TIPO_UNICO, u'Unico'),
        (TIPO_MULTIPLE, u'Multiple')
    )

    establecimiento = models.ForeignKey(
        'establecimientos.Establecimiento', related_name='ultimos_embarazos')
    paciente = models.ForeignKey(
        'pacientes.Paciente', related_name='ultimos_embarazos')
    numero = models.PositiveSmallIntegerField(default=1)
    tipo = models.CharField(
        default=TIPO_UNICO, choices=TIPO_CHOICES, max_length=10)
    embarazo = models.ForeignKey('Embarazo', null=True)
    wawared = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)

    class Meta:
        verbose_name = u'Ultimo embarazo'
        verbose_name_plural = u'Ultimos embarazos'

    print_tipo = print_choices('tipo', TIPO_CHOICES)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(UltimoEmbarazo, self).save(force_insert, force_update, using, update_fields)
        self.paciente.antecedente_obstetrico.generate()

    def delete(self, using=None):
        super(UltimoEmbarazo, self).delete(using)
        if hasattr(self.paciente, 'antecedente_obstetrico'):
            self.paciente.antecedente_obstetrico.generate()

    def bebes_ordered(self):
        return self.bebes.all().order_by('fecha')

    def is_valid_babies_dates_embarazo_multiple(self):
        if self.tipo == self.TIPO_UNICO:
            return True
        else:
            babies = self.bebes.filter().exclude(no_recuerda_fecha=True)
            for baby in babies:
                for other in self.bebes.exclude(Q(id=baby.id) | Q(no_recuerda_fecha=True)):
                    diff = baby.fecha - other.fecha
                    if abs(diff.days) > 9 * 30:
                        return False
        return True

    @classmethod
    def order_by_date(cls, paciente):
        counter = 1
        from django.db.models import get_model
        bebe_class = get_model('embarazos', 'Bebe')
        ids = [ue.id for ue in paciente.ultimos_embarazos.all()]
        for bebe in bebe_class.objects.filter(
                embarazo__paciente=paciente).order_by('fecha'):
            if bebe.embarazo.id in ids:
                bebe.embarazo.numero = counter
                bebe.embarazo.save()
                counter += 1
                ids.remove(bebe.embarazo.id)


class Bebe(models.Model):
    MUERTE_NACIO_MUERTO = 'nacio muerto'
    MUERTE_MENOR_PRIMERA_SEMANA = 'menor primera semana'
    MUERTE_MAYOR_PRIMERA_SEMANA = 'mayor primera semana'
    MUERTE_NO_APLICA = 'no aplica'

    MUERTE_CHOICES = (
        (MUERTE_NO_APLICA, u'No aplica'),
        (MUERTE_NACIO_MUERTO, u'Nacio muerto'),
        (MUERTE_MENOR_PRIMERA_SEMANA, u'< 1ra semana'),
        (MUERTE_MAYOR_PRIMERA_SEMANA, u'> 1ra semana')
    )

    SEXO_MASCULINO = 'M'
    SEXO_FEMENINO = 'F'
    SEXO_NONE = ''

    SEXO_CHOICES = (
        (SEXO_MASCULINO, u'Masculino'),
        (SEXO_FEMENINO, u'Femenino'),
        (SEXO_NONE, '--')
    )

    LACTANCIA_NO_APLICA = 'no aplica'
    LACTANCIA_NO_HUBO = 'no hubo'
    LACTANCIA_MENOS_6_MESES = 'menos 6 meses'
    LACTANCIA_MAS_6_MESES = 'mas 6 meses'

    LACTANCIA_CHOICES = (
        (LACTANCIA_NO_HUBO, u'No hubo'),
        (LACTANCIA_MENOS_6_MESES, u'Menos de 6 meses'),
        (LACTANCIA_MAS_6_MESES, u'6 meses a mas'),
        (LACTANCIA_NO_APLICA, u'No aplica'),
    )

    LUGAR_HOSPITALARIO = 'hospitalario'
    LUGAR_DOMICILIARIO = 'domiciliario'

    LUGAR_CHOICES = (
        (LUGAR_HOSPITALARIO, u'Hospitalario'),
        (LUGAR_DOMICILIARIO, u'Domiciliario')
    )

    ABORTO_COMPLETO = 'completo'
    ABORTO_INCOMPLETO = 'incompleto'
    ABORTO_SEPTICO = 'septico'
    ABORTO_FRUSTO_RETENIDO = 'frusto retenido'
    ABORTO_NO_APLICA = 'no aplica'

    ABORTO_CHOICES = (
        (ABORTO_NO_APLICA, u'No aplica'),
        (ABORTO_COMPLETO, u'Completo'),
        (ABORTO_INCOMPLETO, u'Incompleto'),
        (ABORTO_SEPTICO, u'Séptico'),
        (ABORTO_FRUSTO_RETENIDO, u'Frusto retenido')
    )

    TERMINACION_NO_APLICA = 'no aplica'
    TERMINACION_VAGINAL = 'vaginal'
    TERMINACION_CESAREA = 'cesarea'
    TERMINACION_ABORTO = 'aborto'
    TERMINACION_ABORTO_MOLAR = 'aborto molar'
    TERMINACION_OBITO = 'obito'
    TERMINACION_ECTOPICO = 'ectopico'

    TERMINACION_CHOICES = (
        (TERMINACION_VAGINAL, u'Parto Vaginal'),
        (TERMINACION_CESAREA, u'Cesarea'),
        (TERMINACION_ABORTO, u'Aborto'),
        (TERMINACION_ABORTO_MOLAR, u'Aborto Molar'),
        (TERMINACION_OBITO, u'Obito'),
        (TERMINACION_ECTOPICO, u'Ectópico'),
        (TERMINACION_NO_APLICA, u'No aplica')
    )

    embarazo = models.ForeignKey('UltimoEmbarazo', related_name='bebes')

    terminacion = models.CharField(
        u'Terminacion', max_length=20, choices=TERMINACION_CHOICES,
        default=TERMINACION_VAGINAL)
    vive = models.BooleanField(default=True)
    muerte = models.CharField(
        choices=MUERTE_CHOICES, default=MUERTE_NO_APLICA, max_length=20)
    sexo = models.CharField(
        choices=SEXO_CHOICES, null=True, default=SEXO_NONE, max_length=1,
        blank=True)
    lactancia = models.CharField(
        u'Lactancia', choices=LACTANCIA_CHOICES, default=LACTANCIA_NO_APLICA,
        max_length=20)
    fecha = models.DateField(null=True)
    peso = models.FloatField(null=True, default=0)
    aborto = models.CharField(
        u'Aborto', choices=ABORTO_CHOICES, null=True, default=ABORTO_NO_APLICA,
        max_length=20)
    edad_gestacional = models.SmallIntegerField(default=0)
    lugar = models.CharField(
        u'Lugar', choices=LUGAR_CHOICES, default=LUGAR_HOSPITALARIO,
        max_length=20)
    observacion = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    print_muerte = print_choices('muerte', MUERTE_CHOICES)
    print_sexo = print_choices('sexo', SEXO_CHOICES)
    print_lactancia = print_choices('lactancia', LACTANCIA_CHOICES)
    print_aborto = print_choices('aborto', ABORTO_CHOICES)
    print_lugar = print_choices('lugar', LUGAR_CHOICES)
    print_terminacion = print_choices('terminacion', TERMINACION_CHOICES)
    no_recuerda_fecha = models.BooleanField(u'', default=False)


class PlanParto(models.Model):
    DNI_REGEX = RegexValidator(
        regex=r'[0-9]{8}$', message=u'El DNI debe tener 8 digitos')
    AGE_REGEX = RegexValidator(
        regex=r'[0-9]{1,2}$', message=u'La edad solo debe contener dígitos')

    OTROS = 'otros'

    LUGAR_ATENCION_HOSPITAL = 'hospital'
    LUGAR_ATENCION_CENTRO_SALUD = 'centro salud'
    LUGAR_ATENCION_POSTA_SALUD = 'posta salud'
    LUGAR_ATENCION_DOMICILIO = 'domicilio'
    LUGAR_ATENCION_NO_HA_DECIDICO = 'no ha decidido'

    LUGAR_ATENCION_CHOICES = (
        (LUGAR_ATENCION_HOSPITAL, 'Hospital'),
        (LUGAR_ATENCION_CENTRO_SALUD, 'Centro de salud'),
        (LUGAR_ATENCION_POSTA_SALUD, 'Posta de salud'),
        (LUGAR_ATENCION_DOMICILIO, 'Domicilio'),
        (LUGAR_ATENCION_NO_HA_DECIDICO, 'No ha decidido'),
        (OTROS, 'Otros')
    )

    POSICION_ECHADA = 'echada'
    POSICION_CUCLILLAS = 'cuclillas'
    POSICION_PARADA = 'parada'

    POSICION_CHOICES = (
        (POSICION_ECHADA, 'Echada'),
        (POSICION_CUCLILLAS, 'Cuclillas'),
        (POSICION_PARADA, 'Parada'),
        (OTROS, 'Otros')
    )

    TRANSPORTE_TAXI = 'taxi'
    TRANSPORTE_MOTOTAXI = 'mototaxi'
    TRANSPORTE_MICRO = 'micro'

    TRANSPORTE_CHOICES = (
        (TRANSPORTE_TAXI, 'Taxi'),
        (TRANSPORTE_MOTOTAXI, 'Mototaxi'),
        (TRANSPORTE_MICRO, 'Micro'),
        (OTROS, 'Otros')
    )

    TIPO_SANGRE_CHOICES = 1

    embarazo = models.OneToOneField('Embarazo', related_name='plan_parto')

    donador_1_nombre = models.CharField(max_length=200, blank=True, null=True)
    donador_1_tipo_sangre = models.CharField(
        max_length=20, blank=True, null=True)
    donador_1_domicilio = models.CharField(
        max_length=100, blank=True, null=True)
    donador_1_edad = models.CharField(
        max_length=2, blank=True, null=True, validators=[AGE_REGEX])
    donador_1_parentesco = models.CharField(
        max_length=50, blank=True, null=True)

    donador_2_nombre = models.CharField(max_length=200, blank=True, null=True)
    donador_2_tipo_sangre = models.CharField(
        max_length=20, blank=True, null=True)
    donador_2_domicilio = models.CharField(
        max_length=100, blank=True, null=True)
    donador_2_edad = models.CharField(
        max_length=2, blank=True, null=True, validators=[AGE_REGEX])
    donador_2_parentesco = models.CharField(
        max_length=50, blank=True, null=True)

    establecimiento = models.ForeignKey(
        'establecimientos.Establecimiento', related_name='planes_parto')

    # Entrevista 1

    e1_edad_gestacional = models.CharField(
        max_length=10, blank=True, null=True)
    e1_fecha_probable_parto = models.DateField(null=True, blank=True)
    e1_fecha_probable_parto_observacion = models.CharField(
        max_length=255, null=True, blank=True)
    e1_se_quedara_todo_el_embarazo_en_domicilio_actual = models.BooleanField(
        default=True)
    e1_fecha = models.DateField('Fecha', blank=True, null=True)
    e1_fecha_observacion = models.CharField(
        max_length=255, blank=True, null=True)
    e1_lugar_atencion = models.CharField(
        max_length=20, choices=LUGAR_ATENCION_CHOICES, blank=True)
    e1_lugar_atencion_otros = models.CharField(
        max_length=200, blank=True, null=True)
    e1_lugar_atencion_observacion = models.CharField(
        max_length=255, null=True, blank=True)
    e1_lugar_atencion_razon_eleccion = models.CharField(
        max_length=255, blank=True, null=True)

    e1_distancia_tiempo_llegada = models.CharField(
        max_length=255, blank=True, null=True)

    # Entrevista 2
    e2_edad_gestacional = models.CharField(
        max_length=10, blank=True, null=True)
    e2_fecha = models.DateField(blank=True, null=True)
    e2_fecha_observacion = models.CharField(
        max_length=255, blank=True, null=True)
    e2_lugar_atencion = models.CharField(
        max_length=20, choices=LUGAR_ATENCION_CHOICES, blank=True)
    e2_lugar_atencion_otros = models.CharField(
        max_length=200, blank=True, null=True)
    e2_lugar_atencion_observacion = models.CharField(
        max_length=255, null=True, blank=True)

    e2_posicion_parto = models.CharField(
        max_length=20, choices=POSICION_CHOICES, blank=True)
    e2_posicion_parto_otros = models.CharField(
        max_length=200, blank=True, null=True)
    e2_posicion_parto_observacion = models.CharField(
        max_length=255, blank=True, null=True)

    e2_transporte = models.CharField(
        max_length=20, choices=TRANSPORTE_CHOICES, blank=True)
    e2_transporte_otros = models.CharField(
        max_length=200, blank=True, null=True)
    e2_transporte_observacion = models.CharField(
        max_length=255, blank=True, null=True)

    e2_tiempo_llegada_1 = models.SmallIntegerField(
        u'Tiempo de llegada opción 1', blank=True, null=True)
    e2_tiempo_llegada_2 = models.SmallIntegerField(
        u'Tiempo de llegada opción 2', blank=True, null=True)

    e2_tiempo_llegada_1_observacion = models.CharField(
        max_length=255, blank=True, null=True)
    e2_tiempo_llegada_2_observacion = models.CharField(
        max_length=255, blank=True, null=True)

    e2_persona_que_acompania_en_el_parto = models.CharField(
        max_length=100, blank=True, null=True)
    e2_persona_que_acompania_en_el_parto_observacion = models.CharField(
        max_length=255, blank=True, null=True)

    e2_persona_cuidara_hijos_en_casa = models.CharField(
        max_length=200, blank=True, null=True)
    e2_persona_cuidara_hijos_en_casa_observacion = models.CharField(
        max_length=255, blank=True, null=True)

    # Entrevista 3
    e3_edad_gestacional = models.CharField(
        max_length=10, blank=True, null=True)
    e3_fecha = models.DateField(blank=True, null=True)
    e3_lugar_atencion = models.CharField(
        max_length=20, choices=LUGAR_ATENCION_CHOICES, blank=True)
    e3_lugar_atencion_otros = models.CharField(
        max_length=200, blank=True, null=True)

    e3_posicion_parto = models.CharField(
        max_length=20, choices=POSICION_CHOICES, blank=True)
    e3_posicion_parto_otros = models.CharField(
        max_length=200, blank=True, null=True)

    e3_transporte = models.CharField(
        max_length=20, choices=TRANSPORTE_CHOICES, blank=True)
    e3_transporte_otros = models.CharField(
        max_length=200, blank=True, null=True)

    e3_tiempo_llegada_1 = models.SmallIntegerField(
        u'Tiempo de llegada opción 1', blank=True, null=True)
    e3_tiempo_llegada_2 = models.SmallIntegerField(
        u'Tiempo de llegada opción 2', blank=True, null=True)

    e3_persona_que_acompania_en_el_parto = models.CharField(
        max_length=100, blank=True, null=True)

    e3_persona_cuidara_hijos_en_casa = models.CharField(
        max_length=200, blank=True, null=True)

    edad_gestacional_elegida = models.CharField(
        'EG escogida', max_length=20, blank=True, null=True)

    # observaciones = models.TextField('Observaciones', blank=True)

    vomito_exagerado = models.BooleanField(u'Vómito exagerado', default=False)
    salida_vagina = models.BooleanField(u'Salida de sangre o liquido por su vagina', default=False)
    fiebre_escalofrios = models.BooleanField(u'Fiebre o escalofríos', default=False)
    hinchazon = models.BooleanField(u'Hinchazón de cara , manos y pies', default=False)
    dolor_cabeza_abdominal = models.BooleanField(u'Dolor de cabeza y dolor abdominal', default=False)

    telefono = models.IntegerField(u'Teléfono', blank=True, null=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        ids = []
        if self.e1_fecha:
            control = Control.objects.filter(
                embarazo=self.embarazo,
                atencion_fecha__lte=self.e1_fecha).order_by(
                '-atencion_fecha').first()
            if control:
                self.e1_edad_gestacional = str(
                    control.edad_gestacional_semanas)
                self.e1_fecha_probable_parto = control.fecha_probable_parto
                self.edad_gestacional_elegida = control.eg_elegida
                ids.append(control.id)
        if self.e2_fecha:
            control = Control.objects.filter(
                embarazo=self.embarazo,
                atencion_fecha__lte=self.e2_fecha).exclude(
                id__in=ids).order_by('-atencion_fecha').first()
            if control:
                self.e2_edad_gestacional = str(
                    control.edad_gestacional_semanas)
                self.e1_fecha_probable_parto = control.fecha_probable_parto
                self.edad_gestacional_elegida = control.eg_elegida
                ids.append(control.id)
        if self.e3_fecha:
            control = Control.objects.filter(
                embarazo=self.embarazo,
                atencion_fecha__lte=self.e3_fecha).order_by(
                '-atencion_fecha').first()
            if control:
                self.e3_edad_gestacional = str(
                    control.edad_gestacional_semanas)
                self.e3_fecha_probable_parto = control.fecha_probable_parto
                self.edad_gestacional_elegida = control.eg_elegida
                ids.append(control.id)
        super(PlanParto, self).save(
            force_insert, force_update, using, update_fields)
