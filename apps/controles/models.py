# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from common.util import print_choices

DESCENSO_CEFALICO_CHOICES = (
    ('5', '5/5'),
    ('4', '4/5'),
    ('3', '3/5'),
    ('2', '2/5'),
    ('1', '1/5'),
    ('0', '0/5')
)


class Control(models.Model):
    EG_FUM = 'fum'
    EG_ECOGRAFIA = 'ecografia'
    EG_ALTURA_UTERINA = 'altura uterina'

    EG_CHOICES = (
        (EG_FUM, 'FUM'),
        (EG_ECOGRAFIA, 'Ecografía'),
        (EG_ALTURA_UTERINA, 'Altura Uterina')
    )

    embarazo = models.ForeignKey(
        'embarazos.Embarazo', related_name='controles')
    establecimiento = models.ForeignKey(
        'establecimientos.Establecimiento', related_name='controles')
    paciente = models.ForeignKey(
        'pacientes.Paciente', related_name='controles')
    numero = models.SmallIntegerField(default=0, editable=False)

    atencion_fecha = models.DateField(u'Fecha de atención')
    atencion_hora = models.TimeField(u'Hora de atención')
    eg_fum = models.CharField(
        'EG FUM', max_length=20, default=None, blank=True)
    eg_ecografia = models.CharField(
        'EG ecografía', max_length=20, default=None, blank=True)
    eg_altura_uterina = models.CharField(
        'EG altura uterina', max_length=20, default=None, blank=True)
    eg_elegida = models.CharField(
        'EG escogida', choices=EG_CHOICES, default=EG_FUM, max_length=20,
        blank=True)
    edad_gestacional_semanas = models.CharField(
        max_length=5, blank=True, null=True)
    fecha_probable_parto_fum = models.DateField(
        'FPP FUM', null=True, blank=True)
    fecha_probable_parto_ecografia = models.DateField(
        'FPP ecografia', null=True, blank=True)
    fecha_probable_parto_altura_uterina = models.DateField(
        'FPP altura uterina', null=True, blank=True)

    peso = models.FloatField('Peso actual', default=0, validators=[
        MinValueValidator(20), MaxValueValidator(300)])
    ganancia_peso = models.FloatField('Ganancia de peso', blank=True, null=True)
    imc = models.FloatField('IMC')
    imc_clasificacion = models.CharField(
        'IMC clasificacion', max_length=20, blank=True, null=True)
    temperatura = models.FloatField(
        'Temperatura', null=True, blank=True, validators=[
            MinValueValidator(25), MaxValueValidator(50)])
    presion_sistolica = models.SmallIntegerField(
        'Presion sistolica', null=True, blank=True, validators=[
            MinValueValidator(50), MaxValueValidator(300)])
    presion_diastolica = models.SmallIntegerField(
        'Presion diastolica', null=True, blank=True, validators=[
            MinValueValidator(40), MaxValueValidator(200)])
    frecuencia_respiratoria = models.SmallIntegerField(
        'Frecuencia respiratoria', null=True, blank=True, validators=[
            MinValueValidator(0), MaxValueValidator(180)])
    altura_uterina = models.SmallIntegerField(
        'Altura uterina', blank=True, null=True)
    situacion = models.CharField(
        'Situacion', max_length=20, choices=(
            ('l', 'Longitudinal'),
            ('t', 'Transversal'),
            ('na', 'Indiferente'),), null=True, blank=True)
    presentacion = models.CharField(
        'Presentacion', max_length=20, choices=(
            ('c', 'Cefalico'),
            ('p', 'Podalico'),
            ('na', 'Indiferente'),), null=True, blank=True)
    posicion = models.CharField(
        'Posicion', max_length=20, choices=(
            ('d', 'Derecho'),
            ('i', 'Izquierdo'),
            ('na', 'Indiferente'),), null=True, blank=True)
    leopold = models.CharField('Leopold', max_length=255, blank=True)
    fcf = models.SmallIntegerField('FCF', blank=True, null=True, max_length=3)
    movimientos_fetales = models.CharField(
        'Movimientos fetales', max_length=5, choices=(
            ('sm', 'Sin Movimiento'),
            ('+', '+'),
            ('++', '++'),
            ('+++', '+++'),
            ('na', 'NA'),), null=True, blank=True)
    dinamica_uterina = models.CharField(
        'Dinamica uterina', max_length=5, choices=(
            ('sd', 'Sin Dinamica'),
            ('+', '+'),
            ('++', '++'),
            ('+++', '+++'),
            ('na', 'NA'),), null=True, blank=True)
    proteinuria_cualitativa = models.CharField(
        'proteurina cualitativa', max_length=5, choices=(
            ('-', 'negativo'),
            ('+', '+'),
            ('++', '++'),
            ('+++', '+++'),
            ('nsh', 'No Se Hizo'),), null=True, blank=True)
    edemas = models.CharField(
        'Edemas', max_length=5, choices=(
            ('se', 'Sin Edemas'),
            ('+', '+'),
            ('++', '++'),
            ('+++', '+++'),), null=True, blank=True)
    reflejos = models.CharField(
        'Reflejos', max_length=20, choices=(
            ('0', '0'),
            ('+', '+'),
            ('++', '++'),
            ('+++', '+++'),), null=True, blank=True)
    examen_pezon = models.CharField(
        'Examen pezon', max_length=20, choices=(
            ('formado', 'Formado'),
            ('no formado', 'No Formado'),
            ('sin examen', 'Sin examen'),), null=True, blank=True)
    indicacion_hierro = models.IntegerField(
        'Indicación de Sulfato Ferroso', null=True, blank=True, validators=[
            MinValueValidator(5), MaxValueValidator(100)])
    indicacion_calcio = models.IntegerField(
        'Indicacion Calcio', null=True, blank=True, validators=[
            MinValueValidator(5), MaxValueValidator(100)])
    indicacion_acido_folico = models.IntegerField(
        'Indic Ac. Fólico', null=True, blank=True, validators=[
            MinValueValidator(5), MaxValueValidator(100)])
    indicacion_hierro_acido_folico = models.IntegerField(
        'Indicación de Sulfato Ferroso/Ac Fólico (mayor o igual a 14 semanas)',
        null=True, blank=True, validators=[
            MinValueValidator(5), MaxValueValidator(100)])
    pulso = models.PositiveSmallIntegerField(
        'Pulso', null=True, max_length=2, blank=True, validators=[
            MinValueValidator(0), MaxValueValidator(400)])
    # OC: orientación consejeria
    oc_planificacion_familiar = models.BooleanField(default=False)
    oc_signos_alarma = models.BooleanField(default=False)
    oc_lactancia_materna = models.BooleanField(default=False)
    oc_its = models.BooleanField(default=False)
    oc_nutricion = models.BooleanField(default=False)
    oc_inmunizaciones = models.BooleanField(default=False)
    oc_vih = models.BooleanField(default=False)
    oc_tbc = models.BooleanField(default=False)
    oc_no_se_hizo = models.BooleanField(default=False)
    oc_no_aplica = models.BooleanField(default=False)
    # IC InterConsultas
    ic_psicologia = models.BooleanField(default=False)
    ic_psicologia_fecha_1 = models.DateField(null=True, blank=True)
    ic_psicologia_fecha_2 = models.DateField(null=True, blank=True)
    ic_psicologia_fecha_3 = models.DateField(null=True, blank=True)
    ic_medicina = models.BooleanField(default=False)
    ic_medicina_fecha_1 = models.DateField(null=True, blank=True)
    ic_medicina_fecha_2 = models.DateField(null=True, blank=True)
    ic_medicina_fecha_3 = models.DateField(null=True, blank=True)
    ic_nutricion = models.BooleanField(default=False)
    ic_nutricion_fecha_1 = models.DateField(null=True, blank=True)
    ic_nutricion_fecha_2 = models.DateField(null=True, blank=True)
    ic_nutricion_fecha_3 = models.DateField(null=True, blank=True)
    ic_odontologia = models.BooleanField(default=False)
    ic_odontologia_fecha_1 = models.DateField(null=True, blank=True)
    ic_odontologia_fecha_2 = models.DateField(null=True, blank=True)
    ic_odontologia_fecha_3 = models.DateField(null=True, blank=True)
    ic_enfermeria = models.BooleanField(default=False)
    ic_enfermeria_fecha_1 = models.DateField(null=True, blank=True)
    ic_enfermeria_fecha_2 = models.DateField(null=True, blank=True)
    ic_enfermeria_fecha_3 = models.DateField(null=True, blank=True)
    ic_ecografia = models.BooleanField(default=False)
    ic_ecografia_fecha_1 = models.DateField(null=True, blank=True)
    ic_ecografia_fecha_2 = models.DateField(null=True, blank=True)
    ic_ecografia_fecha_3 = models.DateField(null=True, blank=True)
    ic_laboratorio = models.BooleanField(default=False)
    ic_laboratorio_fecha_1 = models.DateField(null=True, blank=True)
    ic_laboratorio_fecha_2 = models.DateField(null=True, blank=True)
    ic_laboratorio_fecha_3 = models.DateField(null=True, blank=True)

    psicoprofilaxis_fecha_1 = models.DateField(null=True, blank=True)
    psicoprofilaxis_fecha_2 = models.DateField(null=True, blank=True)
    psicoprofilaxis_fecha_3 = models.DateField(null=True, blank=True)
    psicoprofilaxis_fecha_4 = models.DateField(null=True, blank=True)
    psicoprofilaxis_fecha_5 = models.DateField(null=True, blank=True)
    psicoprofilaxis_fecha_6 = models.DateField(null=True, blank=True)

    visita_domiciliaria_fecha_1 = models.DateField(null=True, blank=True)
    visita_domiciliaria_fecha_2 = models.DateField(null=True, blank=True)
    visita_domiciliaria_fecha_3 = models.DateField(null=True, blank=True)
    visita_domiciliaria_fecha_4 = models.DateField(null=True, blank=True)
    visita_domiciliaria_fecha_5 = models.DateField(null=True, blank=True)
    visita_domiciliaria_fecha_6 = models.DateField(null=True, blank=True)
    visita_domiciliaria_actividad_1 = models.CharField(null=True, blank=True, max_length=200)
    visita_domiciliaria_actividad_2 = models.CharField(null=True, blank=True, max_length=200)
    visita_domiciliaria_actividad_3 = models.CharField(null=True, blank=True, max_length=200)
    visita_domiciliaria_actividad_4 = models.CharField(null=True, blank=True, max_length=200)
    visita_domiciliaria_actividad_5 = models.CharField(null=True, blank=True, max_length=200)
    visita_domiciliaria_actividad_6 = models.CharField(null=True, blank=True, max_length=200)

    perfil_biofisico = models.CharField(
        'Perfil biofisico', max_length=20, choices=(
            ('4', '4'),
            ('6', '6'),
            ('8', '8'),
            ('10', '10'),
            ('nsh', 'No se hizo'),
            ('na', 'No aplica'),), blank=True, null=True)
    proxima_cita = models.DateField('Próxima cita', null=True)

    numero_formato_sis = models.CharField(
        'Numero formato SIS', max_length=20, blank=True, null=True)

    asintomatica = models.BooleanField('Asintomática', default=False)

    visito_sintomas = models.BooleanField(default=False)
    visito_diagnosticos = models.BooleanField(default=False)

    zika_viajo = models.CharField(
        max_length=20, choices=(
            ('no', 'No'),
            ('si', 'Si'),), null=True, blank=True)

    zika_pais = models.ForeignKey(
        'ubigeo.Pais', verbose_name=u'País', related_name='zika_pais',
        null=True, blank=True)
    zika_departamento = models.ForeignKey(
        'ubigeo.Departamento', verbose_name=u'Departameto',
        related_name='zina_departamento', null=True, blank=True)
    zika_provincia = models.ForeignKey(
        'ubigeo.Provincia', related_name='zina_provincia',
        verbose_name=u'Provincia', null=True, blank=True)

    zika_sintoma_fiebre = models.BooleanField(
        "Fiebre", blank=True, default=False)
    zika_sintoma_malestar = models.BooleanField(
        "Malestar General", blank=True, default=False)
    zika_sintoma_dolorcabeza = models.BooleanField(
        "Dolor de cabeza", blank=True, default=False)
    zika_sintoma_sarpullido = models.BooleanField(
        "Sarpullido", blank=True, default=False)
    zika_sintoma_conjuntivitis = models.BooleanField(
        "Conjuntivitis", blank=True, default=False)

    # Campo que indica si el control se sincronizo con el sistema de gestion interna del hospital o
    # establecimiento de Salud
    synchronize = models.NullBooleanField()
    # Campo que indica si el control genero su trama Fua para el establecimiento de Salud
    istramafua = models.NullBooleanField()
    fua_numero_asiganado = models.CharField('Numero formato FUA generado', max_length=15, blank=True, null=True)
    fua_identificador_envio_trama = models.IntegerField('FCF', blank=True, null=True, max_length=3)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)

    class Meta:
        verbose_name = u'Atención'
        verbose_name_plural = 'Atenciones'
        ordering = ['numero']
        unique_together = ('embarazo', 'establecimiento', 'paciente', 'atencion_fecha', 'atencion_hora')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.edad_gestacional_semanas = (
            self.calculate_edad_gestacional_semanas())
        values = [self.situacion, self.presentacion, self.posicion]
        self.leopold = '/'.join([val for val in values if val])
        self.imc_clasificacion = self.get_imc_clasificacion()
        super(Control, self).save(
            force_insert, force_update, using, update_fields)

    def get_imc_clasificacion(self):
        if self.imc < 19.8:
            return 'bajo peso'
        elif 19.8 <= self.imc <= 26:
            return 'normal'
        elif 26 < self.imc <= 29:
            return 'sobrepeso'
        else:
            return 'obesidad'

    def generar_tratamiento(self):
        tratamientos = []
        if self.indicacion_hierro:
            tratamientos.append(
                'Sulfato ferroso: {} tabletas'.format(self.indicacion_hierro))
        if self.indicacion_calcio:
            tratamientos.append(
                'Calcio: {} tabletas'.format(self.indicacion_calcio))
        if self.indicacion_acido_folico:
            tratamientos.append(
                'Ácido fólico: {} tabletas'.format(
                    self.indicacion_acido_folico))
        if self.indicacion_hierro_acido_folico:
            tratamientos.append(
                'Sulfato ferroso / ácido fólico: {} tabletas'.format(
                    self.indicacion_hierro_acido_folico))
        return tratamientos

    @property
    def fecha_probable_parto(self):
        if self.eg_elegida == self.EG_FUM:
            return self.fecha_probable_parto_fum
        elif self.eg_elegida == self.EG_ECOGRAFIA:
            return self.fecha_probable_parto_ecografia
        else:
            return self.fecha_probable_parto_altura_uterina

    @property
    def presion_arterial(self):
        if self.presion_sistolica and self.presion_diastolica:
            return '{}/{}'.format(
                self.presion_sistolica, self.presion_diastolica)
        return ''

    def __unicode__(self):
        return 'Control #{numero}  - {paciente}'.format(
            numero=self.numero,
            paciente=self.paciente.nombre_completo
        )

    @property
    def consejerias_realizadas(self):
        ocs = []
        if self.oc_planificacion_familiar:
            ocs.append('Planificación familiar')
        if self.oc_lactancia_materna:
            ocs.append('Lactancia Materna')
        if self.oc_its:
            ocs.append('ITS')
        if self.oc_nutricion:
            ocs.append('Nutrición')
        if self.oc_inmunizaciones:
            ocs.append('Inmunizaciones')
        if self.oc_vih:
            ocs.append('VIH')
        if self.oc_tbc:
            ocs.append('TBC')
        return ocs

    def get_eg(self):
        _format = '{} x {}'
        if self.eg_elegida == self.EG_ECOGRAFIA:
            value = _format.format(self.eg_ecografia, 'ECO')
        elif self.eg_elegida == self.EG_FUM:
            value = _format.format(self.eg_fum, 'FUR')
        else:
            value = _format.format(self.eg_altura_uterina, 'AU')
        return value

    def calculate_edad_gestacional_semanas(self):
        if self.eg_elegida == self.EG_ECOGRAFIA:
            value = self.eg_ecografia
        elif self.eg_elegida == self.EG_FUM:
            value = self.eg_fum
        else:
            value = self.eg_altura_uterina
        eg = 0
        if value:
            try:
                eg = int(value.split()[0])
            except (ValueError, IndexError):
                pass
        return eg

    @classmethod
    def order_by_date(cls, embarazo):
        counter = 1
        for control in embarazo.controles.all().order_by('atencion_fecha'):
            control.numero = counter
            control.save()
            counter += 1

    print_eg_elegida = print_choices('eg_elegida', EG_CHOICES)


class ExamenFisicoFetal(models.Model):
    control = models.ForeignKey('Control', related_name='control', blank=True, null=True)
    medicion_parto = models.ForeignKey('partos.PartogramaMedicion', blank=True, null=True)
    ingreso_parto = models.ForeignKey('partos.Ingreso', blank=True, null=True)
    fcf = models.SmallIntegerField('FCF', blank=True, null=True, max_length=3)
    situacion = models.CharField(
        'Situacion', max_length=20, choices=(
            ('l', 'Longitudinal'),
            ('t', 'Transversal'),
            ('na', 'Indiferente'),), null=True, blank=True)
    presentacion = models.CharField(
        'Presentacion', max_length=20, choices=(
            ('c', 'Cefalico'),
            ('p', 'Podalico'),
            ('na', 'Indiferente'),), null=True, blank=True)
    posicion = models.CharField(
        'Posicion', max_length=20, choices=(
            ('d', 'Derecho'),
            ('i', 'Izquierdo'),
            ('na', 'Indiferente'),), null=True, blank=True)
    movimientos_fetales = models.CharField(
        'Movimientos fetales', max_length=5, choices=(
            ('sm', 'Sin Movimiento'),
            ('+', '+'),
            ('++', '++'),
            ('+++', '+++'),
            ('na', 'NA'),), null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)


class ExamenLaboratorio(models.Model):
    nombre = models.CharField('Nombre', max_length=200, unique=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, editable=False, null=True)

    def __unicode__(self):
        return self.nombre


class Diagnostico(models.Model):
    control = models.OneToOneField('Control', related_name='diagnostico')
    paciente = models.ForeignKey(
        'pacientes.Paciente', related_name='diagnosticos')

    plan_trabajo = models.TextField('Plan de trabajo', blank=True)
    tratamiento = models.TextField('Tratamiento', blank=True)
    tratamiento_2 = models.TextField('Tratamiento 2', blank=True, null=True)
    proxima_cita = models.DateField('Proxima cita', null=True)

    examen_hemoglobina = models.BooleanField('Hemoglobina', default=False)
    examen_hemograma = models.BooleanField('Hemograma', default=False)
    examen_orina = models.BooleanField('Orina', default=False)
    examen_glucosa = models.BooleanField('Glucosa', default=False)
    examen_grupo_sanguineo = models.BooleanField(
        'Grupo sanguineo', default=False)
    examen_factor = models.BooleanField('Factor', default=False)
    otros_examenes = models.ManyToManyField(
        'ExamenLaboratorio', related_name='diagnosticos', blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)

    @property
    def examenes_a_pedir(self):
        examenes = []
        if self.examen_hemoglobina:
            examenes.append('Hemoglobina')
        if self.examen_hemograma:
            examenes.append('Hemograma')
        if self.examen_orina:
            examenes.append('Orina')
        if self.examen_glucosa:
            examenes.append('Glucosa')
        if self.examen_grupo_sanguineo:
            examenes.append('Grupo Sanguineo')
        if self.examen_factor:
            examenes.append('Factor sanguineo')
        for otro_examen in self.otros_examenes.all():
            examenes.append(otro_examen.nombre)
        return ', '.join(examenes)

    def examenes_pendientes(self):  # TODO: validar con el laboratorio
        if not hasattr(self.control, 'laboratorio') and len(self.examenes_a_pedir):
            return False
        return bool(self.examenes_a_pedir)


class DiagnosticoDetalle(models.Model):
    TIPO_D = 'D'
    TIPO_P = 'P'
    TIPO_R = 'R'

    TIPO_CHOICES = (
        (TIPO_D, 'D'),
        (TIPO_P, 'P'),
        (TIPO_R, 'R')
    )

    diagnostico = models.ForeignKey('Diagnostico', null=True, blank=True, related_name='detalles')
    diagnostico_embarazo = models.ForeignKey('partos.TerminacionEmbarazo', null=True, blank=True,
                                             related_name='detalles_puerperio')
    diagnostico_puerperio = models.ForeignKey('puerperio.TerminacionPuerpera', null=True, blank=True,
                                              related_name='detalles_puerperio')
    cie = models.ForeignKey('cie.ICD10')
    tipo = models.CharField('Tipo', max_length=1, choices=TIPO_CHOICES)
    observacion = models.CharField(null=True, blank=True, max_length=200)
    laboratorio = models.CharField('Laboratorio', max_length=100)
    order = models.SmallIntegerField('Orden', default=0)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)

    class Meta:
        ordering = ('order', 'cie__nombre',)


class ProcedimientoDetalle(models.Model):
    diagnostico = models.ForeignKey('Diagnostico', related_name='procedimientos')
    cpt = models.ForeignKey('cpt.CatalogoProcedimiento', null=True)
    observacion = models.CharField(null=True, blank=True, max_length=200)
    order = models.SmallIntegerField('Orden', default=0)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)

    class Meta:
        ordering = ('order', 'cpt__denominacion_procedimientos',)


class Laboratorio(models.Model):
    NO_SE_HIZO = 'no se hizo'
    NO_APLICA = 'no aplica'
    NORMAL = 'normal'
    ANORMAL = 'anormal'
    REACTIVO = 'reactivo'
    NO_REACTIVO = 'no reactivo'
    POSITIVO = 'positivo'
    NEGATIVO = 'negativo'

    NO_NO_CHOICES = (
        (NO_SE_HIZO, 'No se hizo'),
        (NO_APLICA, 'No aplica')
    )

    NORMAL_ANORMAL_CHOICES = (
                                 (NORMAL, 'Normal'),
                                 (ANORMAL, 'Anormal')
                             ) + NO_NO_CHOICES

    NORMAL_ANORMAL_NO_SE_HIZO = (
        (NORMAL, 'Normal'),
        (ANORMAL, 'Anormal'),
        (NO_SE_HIZO, 'No se hizo')
    )

    REACTIVO_NO_REACTIVO_CHOICES = (
                                       (REACTIVO, 'Reactivo'),
                                       (NO_REACTIVO, 'No reactivo')
                                   ) + NO_NO_CHOICES

    POSITIVO_NEGATIVO_CHOICES = (
                                    (POSITIVO, 'Positivo'),
                                    (NEGATIVO, 'Negativo')
                                ) + NO_NO_CHOICES

    POSITIVO_NEGATIVO_NO_SE_HIZO = (
        (POSITIVO, 'Positivo'),
        (NEGATIVO, 'Negativo'),
        (NO_SE_HIZO, 'No se hizo'),
    )

    REACTIVO_NO_REACTIVO_NO_SE_HIZO = (
        (REACTIVO, 'Reactivo'),
        (NO_REACTIVO, 'No reactivo'),
        (NO_SE_HIZO, 'No se hizo')
    )

    GRUPO_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O')
    )

    FACTOR_CHOICES = (
        ('+', '+'),
        ('-', '-'),
        ('- sen desc', '- Sen Desc'),
        ('- no sen', '- No Sen'),
        ('- sen', '- Sen')
    )
    # modifica la propiedad control para que soporte null o blanco ya que este mismo modelo se usara en ingreso de parto
    control = models.OneToOneField('Control', related_name='laboratorio', blank=True, null=True)
    # adiconar los llaves faltantes desde este momento la informacion estara al embarazo activo
    # para redundancia solicitada por MINSA se agregara una llave al paciente
    # aunque no es realmente necesario ya que un embarazo es aun paciente
    embarazo = models.ForeignKey(
        'embarazos.Embarazo', related_name='laboratorios', blank=True, null=True)
    paciente = models.ForeignKey(
        'pacientes.Paciente', related_name='laboratorios', blank=True, null=True)

    grupo = models.CharField(
        'Grupo', max_length=2, choices=GRUPO_CHOICES, blank=True, null=True)
    factor = models.CharField(
        'Factor RH', max_length=10, choices=FACTOR_CHOICES, blank=True,
        null=True)

    rapida_hemoglobina = models.NullBooleanField(
        'Prueba rápida de hemoglobina', default=None)
    rapida_hemoglobina_resultado = models.FloatField(
        'Prueba rápida de hemoglobina', default=None, blank=True, null=True)
    rapida_hemoglobina_fecha = models.DateField('Fecha', null=True, blank=True)

    hemoglobina_1 = models.NullBooleanField('Hemoglobina 1', default=None)
    hemoglobina_1_resultado = models.FloatField(
        'Hemoglobina 1', default=None, blank=True, null=True)
    hemoglobina_1_fecha = models.DateField('Fecha', null=True, blank=True)

    hemoglobina_2 = models.NullBooleanField('Hemoglobina 2', default=None)
    hemoglobina_2_resultado = models.FloatField(
        'Hemoglobina 2 resultado', default=None, blank=True, null=True)
    hemoglobina_2_fecha = models.DateField('Fecha', null=True, blank=True)

    hemoglobina_3 = models.NullBooleanField('Hemoglobina 3', default=None)
    hemoglobina_3_resultado = models.FloatField(
        'Hemoglobina 3 resultado', default=None, blank=True, null=True)
    hemoglobina_3_fecha = models.DateField('Fecha', null=True, blank=True)

    hemoglobina_4 = models.NullBooleanField('Hemoglobina 4', default=None)
    hemoglobina_4_resultado = models.FloatField(
        'Hemoglobina 4 resultado', default=None, blank=True, null=True)
    hemoglobina_4_fecha = models.DateField('Fecha', null=True, blank=True)

    hemoglobina_5 = models.NullBooleanField('Hemoglobina 5', default=None)
    hemoglobina_5_resultado = models.FloatField(
        'Hemoglobina 5 resultado', default=None, blank=True, null=True)
    hemoglobina_5_fecha = models.DateField('Fecha', null=True, blank=True)

    hemoglobina_alta = models.NullBooleanField(
        'Hemoglobina al alta', default=None)
    hemoglobina_alta_resultado = models.FloatField(
        'Hemoglobina alta resultado', default=None, blank=True, null=True)
    hemoglobina_alta_fecha = models.DateField('Fecha', null=True, blank=True)

    glicemia_1 = models.CharField(
        'Glicemia 1', choices=NORMAL_ANORMAL_NO_SE_HIZO, default=NO_SE_HIZO,
        max_length=20)
    glicemia_1_fecha = models.DateField('Fecha', null=True, blank=True)
    glicemia_1_observacion = models.CharField(
        u'Observación', max_length=200, blank=True)

    glicemia_2 = models.CharField(
        'Glicemia 2', choices=NORMAL_ANORMAL_NO_SE_HIZO, default=NO_SE_HIZO,
        max_length=20)
    glicemia_2_fecha = models.DateField('Fecha', null=True, blank=True)
    glicemia_2_observacion = models.CharField(
        u'Observación', max_length=200, blank=True)

    rapida_proteinuria = models.CharField(
        blank=True, choices=REACTIVO_NO_REACTIVO_NO_SE_HIZO,
        default=NO_SE_HIZO, max_length=20, null=True,
        verbose_name=u'Prueba rápida de Proteinuria')
    rapida_proteinuria_fecha = models.DateField(
        blank=True, null=True, verbose_name='Fecha')
    rapida_proteinuria_observacion = models.CharField(
        blank=True, max_length=200, null=True, verbose_name=u'Observación')
    rapida_proteinuria_2 = models.CharField(
        blank=True, choices=REACTIVO_NO_REACTIVO_NO_SE_HIZO,
        default=NO_SE_HIZO, max_length=20, null=True,
        verbose_name=u'Prueba rápida de Proteinuria 2')
    rapida_proteinuria_fecha_2 = models.DateField(
        blank=True, null=True, verbose_name='Fecha')
    rapida_proteinuria_observacion_2 = models.CharField(
        blank=True, max_length=200, null=True, verbose_name=u'Observación')
    rapida_proteinuria_3 = models.CharField(
        blank=True, choices=REACTIVO_NO_REACTIVO_NO_SE_HIZO,
        default=NO_SE_HIZO, max_length=20, null=True,
        verbose_name=u'Prueba rápida de Proteinuria 3')
    rapida_proteinuria_fecha_3 = models.DateField(
        blank=True, null=True, verbose_name='Fecha')
    rapida_proteinuria_observacion_3 = models.CharField(
        blank=True, max_length=200, null=True, verbose_name=u'Observación')

    tolerancia_glucosa = models.CharField(
        'Tolerancia glucosa', choices=NORMAL_ANORMAL_CHOICES,
        default=NO_APLICA, max_length=20)
    tolerancia_glucosa_fecha = models.DateField('Fecha', null=True, blank=True)
    tolerancia_glucosa_observacion = models.CharField(
        u'Observación', max_length=200, blank=True)

    vdrl_rp_1 = models.CharField(
        'VDRL/RPR 1', choices=REACTIVO_NO_REACTIVO_NO_SE_HIZO,
        default=NO_SE_HIZO, max_length=20)
    vdrl_rp_1_fecha = models.DateField('Fecha', null=True, blank=True)
    vdrl_rp_1_observacion = models.CharField(
        u'Observación', max_length=200, blank=True)

    vdrl_rp_2 = models.CharField(
        'VDRL/RPR 2', choices=REACTIVO_NO_REACTIVO_CHOICES,
        default=NO_APLICA, max_length=20)
    vdrl_rp_2_fecha = models.DateField('Fecha', null=True, blank=True)
    vdrl_rp_2_observacion = models.CharField(
        u'Observación', max_length=200, blank=True)

    fta_abs = models.CharField(
        'FTA Abs', choices=REACTIVO_NO_REACTIVO_CHOICES, default=NO_APLICA,
        max_length=20)
    fta_abs_fecha = models.DateField('Fecha', null=True, blank=True)
    fta_abs_observacion = models.CharField(
        u'Observación', max_length=200, blank=True)

    tpha = models.CharField(
        'TPHA', choices=REACTIVO_NO_REACTIVO_CHOICES, default=NO_APLICA,
        max_length=20)
    tpha_fecha = models.DateField('Fecha', null=True, blank=True)
    tpha_observacion = models.CharField(
        u'Observación', max_length=200, blank=True)

    rapida_sifilis = models.CharField(
        u'Rápida sífilis', choices=REACTIVO_NO_REACTIVO_NO_SE_HIZO,
        default=NO_SE_HIZO, max_length=20)
    rapida_sifilis_fecha = models.DateField('Fecha', null=True, blank=True)
    rapida_sifilis_observacion = models.CharField(
        u'Observación', max_length=200, blank=True)

    rapida_sifilis_2 = models.CharField(
        u'Rápida sífilis', choices=REACTIVO_NO_REACTIVO_NO_SE_HIZO,
        default=NO_SE_HIZO, max_length=20)
    rapida_sifilis_2_fecha = models.DateField('Fecha', null=True, blank=True)
    rapida_sifilis_2_observacion = models.CharField(
        u'Observación', max_length=200, blank=True)

    rapida_vih_1 = models.CharField(
        u'Rápida VIH 1', choices=REACTIVO_NO_REACTIVO_NO_SE_HIZO,
        default=NO_SE_HIZO, max_length=20)
    rapida_vih_1_fecha = models.DateField('Fecha', null=True, blank=True)
    rapida_vih_1_observacion = models.CharField(
        u'Observación', max_length=200, blank=True)

    rapida_vih_2 = models.CharField(
        u'Rápida VIH 2', choices=REACTIVO_NO_REACTIVO_CHOICES,
        default=NO_APLICA, max_length=20)
    rapida_vih_2_fecha = models.DateField('Fecha', null=True, blank=True)
    rapida_vih_2_observacion = models.CharField(
        u'Observación', max_length=200, blank=True)

    elisa = models.CharField(
        'ELISA', choices=REACTIVO_NO_REACTIVO_CHOICES, default=NO_APLICA,
        max_length=20)
    elisa_fecha = models.DateField('Fecha', null=True, blank=True)
    elisa_observacion = models.CharField(
        'Observación', max_length=200, blank=True)

    ifi_western_blot = models.CharField(
        'IFI/Western Blot', choices=POSITIVO_NEGATIVO_CHOICES,
        default=NO_APLICA, max_length=20)
    ifi_western_blot_fecha = models.DateField('Fecha', null=True, blank=True)
    ifi_western_blot_observacion = models.CharField(
        u'Observación', max_length=200, blank=True)

    htlv_1 = models.CharField(
        'HTLV 1', choices=POSITIVO_NEGATIVO_CHOICES, default=NO_APLICA,
        max_length=20)
    htlv_1_fecha = models.DateField('Fecha', null=True, blank=True)
    htlv_1_observacion = models.CharField(
        u'Observación', max_length=200, blank=True)

    torch = models.CharField(
        'Torch', choices=POSITIVO_NEGATIVO_CHOICES, default=NO_APLICA,
        max_length=20)
    torch_fecha = models.DateField('Fecha', null=True, blank=True)
    torch_observacion = models.CharField(
        u'Observación', max_length=200, blank=True)

    pcr_zika = models.CharField(
        'PCR Zika', choices=POSITIVO_NEGATIVO_CHOICES, default=NO_APLICA,
        max_length=20)
    pcr_zika_fecha = models.DateField('Fecha', null=True, blank=True)
    pcr_zika_observacion = models.CharField(
        u'Observación', max_length=200, blank=True)

    gota_gruesa = models.CharField(
        'Gota gruesa', choices=POSITIVO_NEGATIVO_CHOICES, default=NO_APLICA,
        max_length=20)
    gota_gruesa_fecha = models.DateField('Fecha', null=True, blank=True)
    gota_gruesa_observacion = models.CharField(
        u'Observación', max_length=200, blank=True)

    malaria_prueba_rapida = models.CharField(
        u'Malaria prueba rápida', choices=POSITIVO_NEGATIVO_CHOICES,
        default=NO_APLICA, max_length=20)
    malaria_prueba_rapida_fecha = models.DateField(
        'Fecha', null=True, blank=True)
    malaria_prueba_rapida_observacion = models.CharField(
        u'Observación', max_length=200, blank=True)

    fluorencia_malaria = models.CharField(
        'Fluorescencia malaria', choices=POSITIVO_NEGATIVO_CHOICES,
        default=NO_APLICA, max_length=20)
    fluorencia_malaria_fecha = models.DateField('Fecha', null=True, blank=True)
    fluorencia_malaria_observacion = models.CharField(
        u'Observación', max_length=200, blank=True)

    examen_completo_orina_1 = models.CharField(
        'Examen completo de orina 1', choices=POSITIVO_NEGATIVO_NO_SE_HIZO,
        default=NO_SE_HIZO, max_length=20)
    examen_completo_orina_fecha_1 = models.DateField(
        'Fecha', null=True, blank=True)
    examen_completo_orina_observacion_1 = models.CharField(
        u'Observación', max_length=200, blank=True)

    examen_completo_orina_2 = models.CharField(
        'Examen completo de orina 2', choices=POSITIVO_NEGATIVO_NO_SE_HIZO,
        default=NO_SE_HIZO, max_length=20)
    examen_completo_orina_fecha_2 = models.DateField(
        'Fecha', null=True, blank=True)
    examen_completo_orina_observacion_2 = models.CharField(
        u'Observación', max_length=200, blank=True)

    leucocituria = models.CharField(
        'Leucocituria', choices=POSITIVO_NEGATIVO_NO_SE_HIZO,
        default=NO_SE_HIZO, max_length=20)
    leucocituria_fecha = models.DateField('Fecha', null=True, blank=True)
    leucocituria_observacion = models.CharField(
        u'Observación', max_length=200, blank=True)

    nitritos = models.CharField(
        'Nitritos', choices=POSITIVO_NEGATIVO_NO_SE_HIZO, default=NO_SE_HIZO,
        max_length=20)
    nitritos_fecha = models.DateField('Fecha', null=True, blank=True)
    nitritos_observacion = models.CharField(
        u'Observación', max_length=200, blank=True)

    urocultivo = models.CharField(
        'Urocultivo', choices=POSITIVO_NEGATIVO_CHOICES, default=NO_APLICA,
        max_length=20)
    urocultivo_fecha = models.DateField('Fecha', null=True, blank=True)
    urocultivo_observacion = models.CharField(
        u'Observación', max_length=200, blank=True)

    bk_en_esputo = models.CharField(
        'BK en esputo', choices=POSITIVO_NEGATIVO_CHOICES, default=NO_APLICA,
        max_length=20)
    bk_en_esputo_fecha = models.DateField('Fecha', null=True, blank=True)
    bk_en_esputo_observacion = models.CharField(
        u'Observación', max_length=200, blank=True)

    listeria = models.CharField(
        'Listeria', choices=POSITIVO_NEGATIVO_CHOICES, default=NO_APLICA,
        max_length=20)
    listeria_fecha = models.DateField('Fecha', null=True, blank=True)
    listeria_observacion = models.CharField(
        u'Observación', max_length=200, blank=True)

    tamizaje_hepatitis_b = models.CharField(
        'Tamizaje hepatitis B', choices=POSITIVO_NEGATIVO_CHOICES,
        default=NO_APLICA, max_length=20)
    tamizaje_hepatitis_b_fecha = models.DateField(
        'Fecha', null=True, blank=True)
    tamizaje_hepatitis_b_observacion = models.CharField(
        u'Observación', max_length=200, blank=True)

    pap = models.CharField(
        'PAP', choices=NORMAL_ANORMAL_NO_SE_HIZO, default=NO_SE_HIZO,
        max_length=20)
    pap_fecha = models.DateField('Fecha', null=True, blank=True)
    pap_observacion = models.CharField(
        u'Observación', max_length=200, blank=True)

    iva = models.CharField(
        'IVA', choices=NORMAL_ANORMAL_CHOICES, default=NO_APLICA,
        max_length=20)
    iva_fecha = models.DateField('Fecha', null=True, blank=True)
    iva_observacion = models.CharField(
        u'Observación', max_length=200, blank=True)

    colposcopia = models.CharField(
        'Colposcopia', choices=NORMAL_ANORMAL_CHOICES, default=NO_APLICA,
        max_length=20)
    colposcopia_fecha = models.DateField('Fecha', null=True, blank=True)
    colposcopia_observacion = models.CharField(
        u'Observación', max_length=200, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)

    @property
    def examenes_con_resultado(self):
        """
        :return: list of results: (label, value, date)
        """
        exs = []
        fields = (
            ('Rápida Sífilis', 'rapida_sifilis', 'rapida_sifilis_fecha',
             'rnr'),
            ('Rápida Sífilis 2', 'rapida_sifilis_2', 'rapida_sifilis_2_fecha',
             'rnr'),
            ('Rápida VIH', 'rapida_vih_1', 'rapida_vih_1_fecha', 'rnr'),
            ('Rápida VIH 2', 'rapida_vih_2', 'rapida_vih_2_fecha', 'rnr'),
            ('Glicemia 1', 'glicemia_1', 'glicemia_1_fecha', 'nan'),
            ('Glicemia 2', 'glicemia_2', 'glicemia_2_fecha', 'nan'),
            ('Examen completo orina 1', 'examen_completo_orina_1',
             'examen_completo_orina_fecha_1', 'pn'),
            ('Examen completo orina 2', 'examen_completo_orina_2',
             'examen_completo_orina_fecha_2', 'pn'),
            ('Leucocituria', 'leucocituria', 'leucocituria_fecha', 'pn'),
            ('Nitritos', 'nitritos', 'nitritos_fecha', 'pn'),
            ('VDRL/RPR 1', 'vdrl_rp_1', 'vdrl_rp_1_fecha', 'rnr'),
            ('VDRL/RPR 2', 'vdrl_rp_2', 'vdrl_rp_2_fecha', 'rnr'),
            ('ELISA', 'elisa', 'elisa_fecha', 'rnr'),
            ('ELISA', 'elisa', 'elisa_fecha', 'rnr'),
            ('PAP', 'pap', 'pap_fecha', 'nan'),
            ('IVA', 'iva', 'iva_fecha', 'nan'),
            ('Colposcopia', 'colposcopia', 'colposcopia_fecha', 'nan'),
            ('IFI/Western Blot', 'ifi_western_blot', 'ifi_western_blot_fecha',
             'pn'),
            ('HTLV 1', 'htlv_1', 'htlv_1_fecha', 'pn'),
            ('TORCH', 'torch', 'torch_fecha', 'pn'),
            ('Gota gruesa', 'gota_gruesa', 'gota_gruesa_fecha', 'pn'),
            ('Malaria prueba rapida', 'malaria_prueba_rapida',
             'malaria_prueba_rapida_fecha', 'pn'),
            ('Fluorescencia malaria', 'fluorencia_malaria',
             'fluorencia_malaria_fecha', 'pn'),
            ('Urocultivo', 'urocultivo', 'urocultivo_fecha', 'pn'),
            ('BK en esputo', 'bk_en_esputo', 'bk_en_esputo_fecha', 'pn'),
            ('Listeria', 'listeria', 'listeria_fecha', 'pn'),
            ('Tamizaje hepatitis B', 'tamizaje_hepatitis_b',
             'tamizaje_hepatitis_b_fecha', 'pn'),
            ('Tolerancia glucosa', 'tolerancia_glucosa',
             'tolerancia_glucosa_fecha', 'nan'),
            ('FTA ABS', 'fta_abs', 'fta_abs_fecha', 'rnr'),
            ('THPA', 'tpha', 'tpha_fecha', 'rnr'),

        )

        if self.grupo:
            exs.append(
                ('Grupo', self.grupo.upper(), False)
            )
        if self.factor:
            exs.append(
                ('Factor', self.factor.upper(), False)
            )
        if self.rapida_hemoglobina and self.rapida_hemoglobina_resultado:
            exs.append(
                ('Rápida hemoglobina', self.rapida_hemoglobina_resultado,
                 self.rapida_hemoglobina_fecha)
            )
        if self.hemoglobina_1 and self.hemoglobina_1_resultado:
            exs.append(
                ('Hemoglobina 1', self.hemoglobina_1_resultado,
                 self.hemoglobina_1_fecha)
            )
        if self.hemoglobina_2 and self.hemoglobina_2_resultado:
            exs.append(
                ('Hemoglobina 2', self.hemoglobina_2_resultado,
                 self.hemoglobina_2_fecha)
            )
        if self.hemoglobina_alta and self.hemoglobina_alta_resultado:
            exs.append(
                ('Hemoglobina al Alta', self.hemoglobina_alta_resultado,
                 self.hemoglobina_alta_fecha)
            )

        for label, field_name, date_field_name, _type in fields:
            value = getattr(self, field_name)
            date_value = getattr(self, date_field_name)
            if _type == 'rnr':
                if value not in (self.REACTIVO, self.NO_REACTIVO):
                    continue
            elif _type == 'nan':
                if value not in (self.NORMAL, self.ANORMAL):
                    continue
            elif _type == 'pn':
                if value not in (self.POSITIVO, self.NEGATIVO):
                    continue
            else:
                continue
            exs.append(
                (label, value.upper(), date_value)
            )
        return exs


class ExamenFisico(models.Model):
    N_A = 'n/a'
    CONSERVADO = 'conservado'
    PATOLOGICO = 'patologico'

    CN_CHOICES = (
        (CONSERVADO, 'Conservado'),
        (PATOLOGICO, 'Patológico'),
        (N_A, 'N/A')
    )

    PELVIMETRIA_ADECUADA = 'adecuada'
    PELVIMETRIA_PELVIS_ESTRECHA = 'pelvis estrecha'

    PELVIMETRIA_CHOICES = (
        (PELVIMETRIA_ADECUADA, 'Adecuada'),
        (PELVIMETRIA_PELVIS_ESTRECHA, 'Pelvis estrecha'),
        (N_A, 'N/A')
    )

    DOLOR_LEVE = 'leve'
    DOLOR_MODERADO = 'moderado'
    DOLOR_SEVERO = 'severo'

    DOLOR_CHOICES = (
        (DOLOR_LEVE, 'Leve'),
        (DOLOR_MODERADO, 'Moderado'),
        (DOLOR_SEVERO, 'Severo'),
        (N_A, 'N/A')
    )

    POSICION_ANTEVERSOFLEXO = 'anteversoflexo'
    POSICION_MEDIO = 'medio'
    POSICION_RETROVERSOFLEXO = 'retroversoflexo'

    POSICION_CHOICES = (
        (POSICION_ANTEVERSOFLEXO, 'Anteversoflexo'),
        (POSICION_MEDIO, 'Medio'),
        (POSICION_RETROVERSOFLEXO, 'Retroversoflexo'),
        (N_A, 'N/A')
    )

    RESTOS_ESCASOS = 'escasos'
    RESTOS_REGULAR = 'regular'
    RESTOS_ABUNDANTE = 'abundante'

    RESTOS_CHOICES = (
        (RESTOS_ESCASOS, 'Escasos'),
        (RESTOS_REGULAR, 'Regular'),
        (RESTOS_ABUNDANTE, 'Abundante'),
        (N_A, 'N/A')
    )

    FONDO_DE_SACO_LIBRE = 'libre'
    FONDO_DE_SACO_OCUPADO = 'ocupado'

    FONDO_DE_SACO_CHOICES = (
        (FONDO_DE_SACO_LIBRE, 'Libre'),
        (FONDO_DE_SACO_OCUPADO, 'Ocupado'),
        (N_A, 'N/A')
    )

    NIVEL_CONCIENCIA_NONE = ''
    NIVEL_CONCIENCIA_LUCIDEZ = 'lucidez'
    NIVEL_CONCIENCIA_OBNUBILACION = 'obnubilacion'
    NIVEL_CONCIENCIA_SOPOR = 'sopor'
    NIVEL_CONCIENCIA_COMA = 'coma'
    NIVEL_CONCIENCIA_OTROS = 'otros'

    NIVEL_CONCIENCIA_CHOICES = (
        (NIVEL_CONCIENCIA_NONE, '----'),
        (NIVEL_CONCIENCIA_LUCIDEZ, 'Lucidez'),
        (NIVEL_CONCIENCIA_OBNUBILACION, 'Obnubilacion'),
        (NIVEL_CONCIENCIA_SOPOR, 'Sopor'),
        (NIVEL_CONCIENCIA_COMA, 'Coma'),
        (NIVEL_CONCIENCIA_OTROS, 'Otros')
    )

    TB_CONSISTENCIA_CHOICES = (
        (0, 'Dura'),
        (1, 'Media'),
        (2, 'Blanda')
    )

    TB_POSICION_CHOICES = (
        (0, 'Posterior'),
        (1, 'Media'),
        (2, 'Anterior')
    )

    TB_BORRAMIENTO_CHOICES = (
        (0, '<30%'),
        (1, '<50%'),
        (2, '<70%'),
        (3, '<100%')
    )

    TB_DILATACION_CHOICES = (
        (0, '0'),
        (1, '1-2 cm'),
        (2, '3-4 cm'),
        (3, '5-6 cm')
    )

    TB_ALTURA_PRESENTACION_CHOICES = (
        (0, 'Libre (-3)'),
        (1, 'Insinuada (-2)'),
        (2, 'Fija (-1/0)'),
        (3, 'Encajada (+1/2)')
    )

    NORMAL = 'normal'
    ANORMAL = 'anormal'
    ESPECULOSCOPIA_CHOICES = (
        (NORMAL, 'Normal'),
        (ANORMAL, 'Anormal'),
    )

    control = models.OneToOneField(Control, related_name='examen_fisico', blank=True, null=True)
    ingreso = models.OneToOneField('partos.Ingreso', related_name='examen_fisico', blank=True, null=True)

    piel_y_mucosas = models.CharField(
        choices=CN_CHOICES, default=N_A, blank=True, max_length=20)
    piel_y_mucosas_observacion = models.CharField(
        'Observacion', max_length=200, blank=True)
    mamas = models.CharField(
        choices=CN_CHOICES, default=N_A, blank=True, max_length=20)
    mamas_observacion = models.CharField(
        'Observacion', max_length=200, blank=True)
    respiratorio = models.CharField(
        choices=CN_CHOICES, default=N_A, blank=True, max_length=20)
    respiratorio_observacion = models.CharField(
        'Observacion', max_length=200, blank=True)
    cardiovascular = models.CharField(
        choices=CN_CHOICES, default=N_A, blank=True, max_length=20)
    cardiovascular_observacion = models.CharField(
        'Observacion', max_length=200, blank=True)
    odontologico = models.CharField(
        choices=CN_CHOICES, default=N_A, blank=True, max_length=20)
    odontologico_observacion = models.CharField(
        'Observacion', max_length=200, blank=True)
    abdomen = models.CharField(
        choices=CN_CHOICES, default=N_A, blank=True, max_length=20)
    abdomen_observacion = models.CharField(
        'Observacion', max_length=200, blank=True)
    urinario = models.CharField(
        choices=CN_CHOICES, default=N_A, blank=True, max_length=20)
    urinario_observacion = models.CharField(
        'Observacion', max_length=200, blank=True)
    neurologico = models.CharField(
        choices=CN_CHOICES, default=N_A, blank=True, max_length=20)
    neurologico_observacion = models.CharField(
        'Observacion', max_length=200, blank=True)

    nivel_conciencia = models.CharField(
        'Nivel de conciencia', choices=NIVEL_CONCIENCIA_CHOICES,
        default=NIVEL_CONCIENCIA_NONE, max_length=20, blank=True)
    nivel_conciencia_otros = models.CharField(
        'Nivel Conciencia otros', max_length=200, null=True, blank=True)

    especuloscopia = models.NullBooleanField(
        'Especuloscopía', default=None, blank=True)

    especuloscopia_vagina = models.CharField(
        'Vagina', max_length=100, blank=True)
    especuloscopia_cervix = models.CharField(
        'Cervix', max_length=100, blank=True)
    especuloscopia_fondo_de_saco = models.CharField(
        'Fondo de saco', max_length=100, blank=True)
    especuloscopia_observaciones = models.CharField(
        'Observaciones', max_length=100, blank=True)

    # Tacto vaginal
    tv_cambio_cervicales = models.NullBooleanField(
        'Cambios cervicales', default=None, blank=True)

    # test de bishop
    tv_tb_aplica = models.BooleanField(
        '¿Aplica Test de Bishop?', default=False)
    tv_tb_consistencia = models.SmallIntegerField(
        'Consistencia', default=None, choices=TB_CONSISTENCIA_CHOICES,
        blank=True, null=True)
    tv_tb_posicion = models.SmallIntegerField(
        'Posición', default=None, choices=TB_POSICION_CHOICES, blank=True,
        null=True)
    tv_tb_borramiento = models.SmallIntegerField(
        'Borramiento', default=None, choices=TB_BORRAMIENTO_CHOICES,
        blank=True, null=True)
    tv_tb_dilatacion = models.SmallIntegerField(
        'Dilatación', default=None, choices=TB_DILATACION_CHOICES,
        blank=True, null=True)
    tv_tb_altura_presentacion = models.SmallIntegerField(
        'Altura presentación', default=None,
        choices=TB_ALTURA_PRESENTACION_CHOICES, blank=True, null=True)
    tv_tb_resultado = models.SmallIntegerField(
        'Escala de Bishop', default=None, blank=True, null=True)

    tv_vagina = models.CharField('Vagina', max_length=100, blank=True)
    tv_utero = models.CharField('Utero', max_length=100, blank=True)
    tv_hallazgos = models.CharField('Hallazgos', max_length=200, blank=True)
    tv_otros = models.CharField('Anexos', max_length=200, blank=True)

    tv_dilatacion = models.SmallIntegerField(
        'Dilatación', blank=True, null=True, choices=(
            (n, str(n)) for n in range(0, 11)))
    tv_incorporacion = models.CharField(
        'Incorporación', max_length=20, blank=True, choices=(
            ('-40%', 'menos de 40%'),
            ('50%', '50%'),
            ('70%', '70%'),
            ('80%', '80%'),
            ('90%', '90%'),
            ('100%', '100%'),))
    tv_altura_presentacion = models.CharField(
        'Altura de presentación', max_length=5, blank=True, null=True,
        choices=DESCENSO_CEFALICO_CHOICES)
    tv_membranas = models.CharField(
        'Membranas', max_length=10, choices=(
            ('integras', 'Íntegras'),
            ('rotas', 'Rotas'),), blank=True)
    tv_membranas_rotas_tipo = models.CharField('', max_length=10, choices=(
        ('artificial', 'Artificial'),
        ('espontanea', 'Espontanea')
    ), blank=True)
    tv_membranas_rotas_tiempo = models.FloatField('Tiempo', null=True, blank=True, validators=[
        MinValueValidator(0), MaxValueValidator(48)
        ])
    tv_liquido_amniotico = models.CharField(
        u'Líquido amniótico', max_length=20, choices=(
            ('claro', 'Claro'),
            ('meconial', 'Meconial'),
            ('sanguinolento', 'Sanguinolento')
        ), blank=True, null=True)

    pelvimetria = models.CharField(
        u'Pelvimetría', choices=PELVIMETRIA_CHOICES, default=N_A,
        max_length=20)
    pelvimetria_observacion = models.CharField(
        u'Observación', max_length=100, blank=True)

    examen_ginecologico = models.NullBooleanField(
        u'Examen ginecológico', default=None, blank=True)

    # Exame ginecologico
    eg_dolor = models.CharField(
        'Dolor', choices=DOLOR_CHOICES, default=N_A, blank=True, max_length=20)
    eg_posicion = models.CharField(
        u'Posición', choices=POSICION_CHOICES, default=N_A, blank=True,
        max_length=20)
    eg_restos = models.CharField(
        'Restos', choices=RESTOS_CHOICES, default=N_A, blank=True,
        max_length=20)
    eg_culdocentesis = models.NullBooleanField(
        'Culdocentesis', default=None, blank=True)
    eg_fondo_de_saco = models.CharField(
        'Fondo de saco', choices=FONDO_DE_SACO_CHOICES, default=N_A,
        blank=True, max_length=20)
    eg_mal_olor = models.NullBooleanField('Mal olor', default=None, blank=True)
    eg_vulvas = models.CharField('Vulva', max_length=200, blank=True)
    eg_genitales_externos = models.CharField(
        'Genitales externos', max_length=200, blank=True)
    eg_vagina = models.CharField('Vagina', max_length=200, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)

    print_piel_y_mucosas = print_choices('piel_y_mucosas', CN_CHOICES)
    print_mamas = print_choices('mamas', CN_CHOICES)
    print_respiratorio = print_choices('respiratorio', CN_CHOICES)
    print_cardiovascular = print_choices('cardiovascular', CN_CHOICES)
    print_odontologico = print_choices('odontologico', CN_CHOICES)
    print_abdomen = print_choices('abdomen', CN_CHOICES)
    print_urinario = print_choices('urinario', CN_CHOICES)
    print_neurologico = print_choices('neurologico', CN_CHOICES)
    print_nivel_conciencia = print_choices(
        'nivel_conciencia', NIVEL_CONCIENCIA_CHOICES)
    print_eg_dolor = print_choices('eg_dolor', DOLOR_CHOICES)
    print_eg_posicion = print_choices('eg_posicion', POSICION_CHOICES)
    print_eg_restos = print_choices('eg_restos', RESTOS_CHOICES)
    print_eg_fondo_de_saco = print_choices(
        'eg_fondo_de_saco', NIVEL_CONCIENCIA_CHOICES)
    print_pelvimetria = print_choices('pelvimetria', PELVIMETRIA_CHOICES)

    def es_conservado(self):
        return self.piel_y_mucosas != self.PATOLOGICO and \
               self.mamas != self.PATOLOGICO and \
               self.respiratorio != self.PATOLOGICO and \
               self.cardiovascular != self.PATOLOGICO and \
               self.odontologico != self.PATOLOGICO and \
               self.abdomen != self.PATOLOGICO and \
               self.urinario != self.PATOLOGICO and \
               self.neurologico != self.PATOLOGICO and \
               self.nivel_conciencia == self.NIVEL_CONCIENCIA_NONE and \
               self.tv_cambio_cervicales is None and \
               not self.tv_tb_resultado and \
               not self.tv_hallazgos and \
               not self.tv_incorporacion and \
               not self.tv_liquido_amniotico and \
               not self.tv_membranas and \
               not self.tv_otros and \
               self.pelvimetria == self.N_A and \
               self.eg_dolor == self.N_A and \
               self.eg_posicion == self.N_A and \
               self.eg_restos == self.N_A and \
               self.eg_culdocentesis is None and \
               self.eg_fondo_de_saco == self.N_A and \
               self.eg_mal_olor is None and \
               not self.eg_vulvas and \
               not self.eg_vagina and \
               not self.eg_genitales_externos

    def resume(self):
        data = {
            'patologicos': [],
            'ginecologicos': []
        }

        if self.piel_y_mucosas == self.PATOLOGICO:
            data['patologicos'].append({
                'nombre': 'Piel y mucosas',
                'observacion': self.piel_y_mucosas_observacion
            })
        if self.mamas == self.PATOLOGICO:
            data['patologicos'].append({
                'nombre': 'Mamas',
                'observacion': self.mamas_observacion
            })
        if self.respiratorio == self.PATOLOGICO:
            data['patologicos'].append({
                'nombre': 'Respiratorio',
                'observacion': self.respiratorio_observacion
            })
        if self.cardiovascular == self.PATOLOGICO:
            data['patologicos'].append({
                'nombre': 'Cardiovascular',
                'observacion': self.cardiovascular_observacion
            })
        if self.odontologico == self.PATOLOGICO:
            data['patologicos'].append({
                'nombre': 'Odontológico',
                'observacion': self.odontologico_observacion
            })
        if self.abdomen == self.PATOLOGICO:
            data['patologicos'].append({
                'nombre': 'Abdomen',
                'observacion': self.abdomen_observacion
            })
        if self.urinario == self.PATOLOGICO:
            data['patologicos'].append({
                'nombre': 'Urinario',
                'observacion': self.urinario_observacion
            })
        if self.neurologico == self.PATOLOGICO:
            data['patologicos'].append({
                'nombre': 'Neurológico',
                'observacion': self.neurologico_observacion
            })

        if self.eg_dolor != self.N_A:
            data['ginecologicos'].append({
                'nombre': 'Dolor',
                'valor': self.print_eg_dolor()
            })
        if self.eg_posicion != self.N_A:
            data['ginecologicos'].append({
                'nombre': 'Posicion',
                'valor': self.print_eg_posicion()
            })
        if self.eg_restos != self.N_A:
            data['ginecologicos'].append({
                'nombre': 'Restos',
                'valor': self.print_eg_restos()
            })
        if self.eg_fondo_de_saco != self.N_A:
            data['ginecologicos'].append({
                'nombre': 'Fondo de saco',
                'valor': self.print_eg_fondo_de_saco()
            })
        if self.eg_culdocentesis is not None:
            tmp = {
                'nombre': 'Culdocentesis',
                'valor': 'Si'
            }
            if not self.eg_culdocentesis:
                tmp['valor'] = 'No'
            data['ginecologicos'].append(tmp)
        if self.eg_mal_olor is not None:
            tmp = {
                'nombre': 'Mal olor',
                'valor': 'Si'
            }
            if not self.eg_mal_olor:
                tmp['valor'] = 'No'
            data['ginecologicos'].append(tmp)
        return data


class Sintoma(models.Model):
    control = models.ForeignKey('Control', related_name='sintomas', blank=True, null=True)
    ingreso = models.ForeignKey('partos.Ingreso', related_name='sintomas_ingreso', blank=True, null=True)
    cie = models.ForeignKey('cie.ICD10')
    observacion = models.CharField(
        'Observación',
        max_length=200,
        blank=True,
        null=True,
        default=None
    )

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)

    class Meta:
        ordering = ('cie__nombre_mostrar', 'cie__nombre')
