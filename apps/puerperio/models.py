# coding: utf-8

from __future__ import unicode_literals

from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from django.db import models
from django.conf import settings


class RecienNacido(models.Model):

    SEXO_MASCULINO = 'm'
    SEXO_FEMENINO = 'f'
    SEXO_INDETERMINADO = 'indeterminado'

    SEXO_CHOICES = (
        (SEXO_MASCULINO, u'Masculino'),
        (SEXO_FEMENINO, u'Femenino'),
        (SEXO_INDETERMINADO, 'Indeterminado')
    )

    PESO_EG_ADECUADO = 'adecuado'
    PESO_EG_PEQUENO = 'pequeño'
    PESO_EG_GRANDE = 'grande'

    PESO_EG_CHOICES = (
        (PESO_EG_ADECUADO, 'Adecuado'),
        (PESO_EG_PEQUENO, 'Pequeño'),
        (PESO_EG_GRANDE, 'Grande')
    )

    EXAMEN_FISICO_NORMAL = 'normal'
    EXAMEN_FISICO_ANORMAL = 'anormal'

    EXAMEN_FISICO_CHOICES = (
        (EXAMEN_FISICO_NORMAL, 'Normal'),
        (EXAMEN_FISICO_ANORMAL, 'Anormal')
    )

    terminacion_embarazo = models.ForeignKey(
        'partos.TerminacionEmbarazo', related_name='recien_nacidos')
    nombres = models.CharField(u'Nombres', max_length=100, null=True)
    apellido_paterno = models.CharField(
        u'Apellido Paterno', max_length=50, null=True)
    apellido_materno = models.CharField(
        u'Apellido Materno', max_length=50, null=True)
    sexo = models.CharField('Sexo', max_length=2, choices=SEXO_CHOICES)
    peso = models.SmallIntegerField('Peso', validators=[
        MinValueValidator(100), MaxValueValidator(9999)
    ])
    vive = models.BooleanField('¿Vive?', default=True)
    temperatura = models.FloatField('Temperatura', validators=[
        MinValueValidator(25), MaxValueValidator(50)
    ])
    perimetro_cefalico = models.IntegerField(
        'Perímetro cefálico', null=True, blank=True)
    perimetro_toraxico = models.IntegerField(
        'Perímetro toráxico', null=True, blank=True)
    talla = models.FloatField('Talla')
    edad_por_examen_fisico = models.SmallIntegerField('Edad por examen físico', blank=True, null=True, validators=[
        MinValueValidator(10), MaxValueValidator(99)
    ])
    peso_por_edad_gestacional = models.CharField(
        'Peso por edad gestacional', max_length=20, choices=PESO_EG_CHOICES, default=PESO_EG_ADECUADO)
    apgar_1 = models.SmallIntegerField('APGAR 1\'', blank=True, null=True, validators=[
        MinValueValidator(0), MaxValueValidator(10)
    ])
    apgar_5 = models.SmallIntegerField('APGAR 5\'', blank=True, null=True, validators=[
        MinValueValidator(0), MaxValueValidator(10)
    ])
    examen_fisico = models.CharField(
        'Examen Físico', max_length=10, choices=EXAMEN_FISICO_CHOICES, default=EXAMEN_FISICO_NORMAL)
    necropsia = models.NullBooleanField('Necropsia', default=None)
    hospitalizacion = models.BooleanField('Hospitalización', default=False)

    tiene_egreso = models.BooleanField(default=False)

    # can: condicion al nacer
    can_llanto_inmediato = models.BooleanField(
        'Llanto inmediato', default=False)
    can_cianotico = models.BooleanField('Cianótico', default=False)
    can_palido = models.BooleanField('Pálido', default=False)
    can_pletorico = models.BooleanField('Pletórico', default=False)
    can_flacido = models.BooleanField('Flácido', default=False)
    can_circular = models.BooleanField('Circular', default=False)
    can_asfixia = models.BooleanField('Asfixia al nacer', default=False)
    can_asfixia_severa = models.BooleanField('Asfixia severa', default=False)
    can_impregnacion_meconial = models.BooleanField(
        'Impregnación. Meconial', default=False)
    can_caput = models.BooleanField('Caput', default=False)
    can_cefalohematoma = models.BooleanField('Cefalohematoma', default=False)
    can_edematoso = models.BooleanField('Edematoso', default=False)
    can_ictericia = models.BooleanField('Ictericia', default=False)

    tiene_malformaciones_congenitas = models.BooleanField(
        '¿Tiene malformaciones congénitas?', default=False)

    # mc: malformaciones congenitas
    mc_sindrome_de_down = models.BooleanField(
        'Síndrome de Down', default=False)
    mc_siames = models.BooleanField('Siames', default=False)
    mc_labio_leporino = models.BooleanField('Labio Leporino', default=False)
    mc_paladar_rendido = models.BooleanField('Paladar rendido', default=False)
    mc_polidactilia = models.BooleanField('Polidactilia', default=False)

    # ai: atención inmediata
    ai_aspiracion_oro_nasal = models.BooleanField(
        'Aspiración oro nasal', default=False)
    ai_aspiracion_endotraqueal = models.BooleanField(
        'Aspiración endotraqueal', default=False)
    ai_ventilacion_asistida = models.BooleanField(
        'Ventilación asistida', default=False)
    ai_oxigeno = models.BooleanField('Oxigeno', default=False)
    ai_masaje_cardiaco = models.BooleanField('Masaje cardiaco', default=False)
    ai_bicarbonato = models.BooleanField('Bicarbonato', default=False)
    ai_adrenalina = models.BooleanField('Adrenalina', default=False)

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='recien_nacidos_c')
    modifier = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='recien_nacidos_m')

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    @property
    def nombre_completo(self):
        return '{} {} {}'.format(self.nombres, self.apellido_paterno, self.apellido_materno)


class Monitoreo(models.Model):

    ABIERTO = 'abierto'
    CERRADO = 'cerrado'

    establecimiento = models.ForeignKey('establecimientos.Establecimiento', null=True, related_name='monitoreos')
    paciente = models.ForeignKey('pacientes.Paciente', related_name='monitoreos')
    embarazo = models.OneToOneField('embarazos.Embarazo', related_name='monitoreos')
    terminacion_embarazo = models.OneToOneField('partos.TerminacionEmbarazo', related_name='monitoreo_puerperio')

    status = models.CharField(max_length=20, default=ABIERTO)

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='monitoreo_c')
    modifier = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='monitoreo_m')

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)


class MonitoreoMedicion(models.Model):

    FORMADO = 'formado'
    UMBILICADO = 'umbilicado'
    PLANO = 'plano'
    BLANDAS = 'blandas'
    TURGENTES = 'turgentes'
    SECRETANTES = 'secretantes'
    CONTRAIDO = 'contraido'
    NO_CONTRAIDO = 'no contraido'
    HEMATICOS = 'hematicos'
    SERO_HEMATICOS = 'serohematicos'
    SEROSOS = 'serosos'
    MAL_OLOR = 'mal olor'
    SIN_OLOR = 'sin olor'
    MEDIO_LATERAL_IZQUIERDA = 'medio lateral izquierda'
    MEDIO_LATERAL_DERECHA = 'medio lateral derecha'
    CON_EDEMA = 'con edema'
    DEHISENCIA_HERIDA = 'dehisencia de herida'
    BORDES_AFRONTADOS = 'bordes afrontados'
    BORDES_NO_AFRONTADOS = 'bordes no afrontados'
    DOLOROSO = 'doloroso'
    NO_SE_HIZO = 'no se hizo'
    NO_APLICA = 'no aplica'
    REACTIVO = 'reactivo'
    NO_REACTIVO = 'no reactivo'

    NO_NO_CHOICES = (
        (NO_SE_HIZO, 'No se hizo'),
        (NO_APLICA, 'No aplica')
    )

    MAMAS_PEZON_CHOICES = (
        (FORMADO, 'Formado'),
        (UMBILICADO, 'Umbilicado'),
        (PLANO, 'Plano')
    )

    MAMAS_CARACTERISTICAS_CHOICES = (
        (BLANDAS, 'Blandas'),
        (TURGENTES, 'Turgentes'),
        (SECRETANTES, 'Secretantes')
    )

    UTERO_CARACTERISTICAS_CHOICES = (
        (CONTRAIDO, 'Contraido'),
        (NO_CONTRAIDO, 'No contraido')

    )

    UTERO_UBICACION_CHOICES = (
        ('3cm encima', 'A 3cm por encima'),
        ('2cm encima', 'A 2cm por encima'),
        ('1cm encima', 'A 1cm por encima'),
        ('nivel cicatriz', 'A nivel de la cicatriz'),
        ('1cm debajo', 'A 1cm por debajo'),
        ('2cm debajo', 'A 2cm por debajo'),
        ('3cm debajo', 'A 3cm por debajo')
    )

    LOQUIOS_CARACTERISTICAS_CHOICES = (
        (HEMATICOS, 'Hematicos'),
        (SERO_HEMATICOS, 'Sero-hematicos'),
        (SEROSOS, 'Serosos')
    )

    LOQUIOS_CANTIDAD_CHOISES = (
        ('+', '+'),
        ('++', '++'),
        ('+++', '+++')
    )

    LOQUIOS_OLOR_CHOISES = (
        (MAL_OLOR, 'Mal olor'),
        (SIN_OLOR, 'Sin olor')
    )

    EPISEOTOMIA_TIPO_CHOISES = (
        (MEDIO_LATERAL_DERECHA, 'Medio lateral derecha'),
        (MEDIO_LATERAL_IZQUIERDA, 'Medio lateral izquierda'),
        (CON_EDEMA, 'Con edema'),
        (DEHISENCIA_HERIDA, 'Dehisencia de herida')
    )

    PURULENTO = 'purulento'
    INFECTADA = 'infectada'
    FLOGOSIS = 'flogosis'
    SIN_DOLOR = 'sin dolor'

    EPISEOTOMIA_CARACTERISTICAS_CHOISES = (
        (BORDES_AFRONTADOS, 'Bordes afrontados'),
        (BORDES_NO_AFRONTADOS, 'Bordes no afrontados'),
        (DOLOROSO, 'Doloroso'),
        (PURULENTO, 'Purulento'),
        (INFECTADA, 'Infectada'),
        (FLOGOSIS, 'Flogosis'),
        (SIN_DOLOR, 'Sin dolor')
    )

    VP_CL = 'cl na'
    VP_DEXTROZA = 'dextroza'
    VP_HEMACELL = 'hemacell'

    VP_CHOICES = (
        (VP_CL, 'Cl Na'),
        (VP_DEXTROZA, 'Dextroza'),
        (VP_HEMACELL, 'Hemacell')
    )

    REACTIVO_NO_REACTIVO_CHOICES = (
        (REACTIVO, 'Reactivo'),
        (NO_REACTIVO, 'No reactivo')
    ) + NO_NO_CHOICES

    fecha = models.DateField('Fecha')
    hora = models.TimeField('Hora')

    monitoreo = models.ForeignKey('Monitoreo', related_name='mediciones')
    establecimiento = models.ForeignKey(
        'establecimientos.Establecimiento', related_name='mediciones')

    # Funciones vitales
    presion_sistolica = models.SmallIntegerField('Presion sistolica', null=True, blank=True, validators=[
        MinValueValidator(0), MaxValueValidator(300)
    ])
    presion_diastolica = models.SmallIntegerField('Presion diastolica', null=True, blank=True, validators=[
        MinValueValidator(0), MaxValueValidator(200)
    ])
    pulso = models.PositiveSmallIntegerField('Pulso', null=True, max_length=2, blank=True, validators=[
        MinValueValidator(0), MaxValueValidator(400)
    ])
    frecuencia_respiratoria = models.SmallIntegerField('Frecuencia respiratoria', null=True, blank=True, validators=[
        MinValueValidator(1), MaxValueValidator(180)
    ])
    temperatura = models.FloatField('Temperatura', null=True, blank=True, validators=[
        MinValueValidator(25), MaxValueValidator(50)
    ])

    mamas_pezon = models.CharField('Pezon', max_length=10, choices=MAMAS_PEZON_CHOICES, blank=False, null=True)
    mamas_caracteristicas = models.CharField('Caracteristicas', max_length=11, choices=MAMAS_CARACTERISTICAS_CHOICES,
                                             blank=False, null=True)

    utero_caracteristicas = models.CharField(
        'Caracteristicas', max_length=12, choices=UTERO_CARACTERISTICAS_CHOICES,
                                                blank=False, null=True)
    utero_ubicacion = models.CharField(
        'Ubicacion', max_length=30, choices=UTERO_UBICACION_CHOICES,
                                                blank=False, null=True)

    loquios_caracteristicas = models.CharField(
        'Caracteristicas', max_length=14, choices=LOQUIOS_CARACTERISTICAS_CHOICES,
                                                blank=False, null=True)
    loquios_cantidad = models.CharField(
        'Cantidad', max_length=3, choices=LOQUIOS_CANTIDAD_CHOISES, blank=False, null=True)
    loquios_olor = models.CharField(
        'Olor', max_length=10, choices=LOQUIOS_OLOR_CHOISES, blank=False, null=True)

    episeotomia_tipo = models.CharField(
        'Tipo', max_length=30, choices=EPISEOTOMIA_TIPO_CHOISES,
                                                blank=False, null=True)
    episeotomia_caracteristicas = models.CharField('Caracteristicas', max_length=30,
                                                choices=EPISEOTOMIA_CARACTERISTICAS_CHOISES, blank=False, null=True)
    via_periferica = models.NullBooleanField(verbose_name='Vía periférica', default=None)
    vp_tipo_de_solucion = models.CharField('Tipo de solución', max_length=30, choices=VP_CHOICES,
                                                blank=False, null=True)
    vp_oxitocina = models.NullBooleanField(verbose_name='Oxitocina', default=None)
    vp_cantidad = models.FloatField('Cantidad', null=True, blank=True, validators=[
        MinValueValidator(0), MaxValueValidator(9999)
    ])
    lab_hemoglobina_post_parto = models.FloatField(
        'Hemoglobina post parto', null=True, blank=True, validators=[
            MinValueValidator(0), MaxValueValidator(99)
        ])
    lab_fecha_hemoglobina = models.DateField('Fecha', null=True, blank=True)
    lab_elisa = models.CharField('ELISA', choices=REACTIVO_NO_REACTIVO_CHOICES, default=NO_APLICA,
        max_length=20)
    lab_elisa_fecha = models.DateField('Fecha', null=True, blank=True)
    lab_rpr = models.CharField('RPR', choices=REACTIVO_NO_REACTIVO_CHOICES, default=NO_APLICA,
        max_length=20)
    lab_rpr_fecha = models.DateField('Fecha', null=True, blank=True)

    alojamiento_conjunto = models.NullBooleanField(verbose_name='Alojamiento conjunto', default=None)
    alojamiento_conjunto_observacion = models.TextField(verbose_name='Observación', blank=True, null=True)
    contacto_piel = models.NullBooleanField(verbose_name='Contacto piel a piel', default=None)
    contacto_piel_observacion = models.TextField(verbose_name='Observación', blank=True, null=True)

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='monitoreo_medicion_c')
    modifier = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tmonitoreo_medicion_m')

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ('fecha', 'hora')


class EgresoGestante(models.Model):

    TIPO_EGRESO_CHOICES = (
        ('sano', 'Sano'),
        ('traslado', 'Traslado'),
        ('con patologia', 'Con patologia'),
        ('fallece', 'Fallece')
    )

    establecimiento = models.ForeignKey('establecimientos.Establecimiento', related_name='gestante_egresos')
    paciente = models.ForeignKey('pacientes.Paciente', related_name='gestante_egresos')
    ingreso = models.OneToOneField('partos.Ingreso', related_name='egreso_gestante')
    terminacion_embarazo = models.OneToOneField('partos.TerminacionEmbarazo', related_name='egreso_gestante')

    fecha = models.DateField('Fecha')
    hora = models.TimeField('Hora')

    tipo = models.CharField(
        'Egreso', max_length=20, choices=TIPO_EGRESO_CHOICES, null=True)

    diagnostico = models.ForeignKey(
        'cie.ICD10Base', related_name='egreso_gestante_diagnostico')
    diagnostico_traslado = models.ForeignKey(
        'cie.ICD10Base', related_name='egreso_gestante_diagnostico_traslado', blank=True, null=True)
    diagnostico_fallecimiento = models.ForeignKey(
        'cie.ICD10Base', related_name='egreso_gestante_diagnostico_fallecimiento', blank=True, null=True)

    establecimiento_traslado = models.CharField(
        'Establecimiento traslado', max_length=50, blank=True, null=True)

    diagnostico_str = models.CharField(
        max_length=255, editable=False, null=True)
    diagnostico_traslado_str = models.CharField(
        max_length=255, editable=False, null=True)
    diagnostico_fallecimiento_str = models.CharField(
        max_length=255, editable=False, null=True)

    # ANT: anticonceptivos
    ant_ligadura_tubaria = models.BooleanField(
        'Ligadura Tubaria', default=False, blank=True)
    ant_anticoncec_combinada = models.BooleanField(
        'Anticoncec. Combinada', default=False, blank=True)
    ant_abstinencia_periodica = models.BooleanField(
        'Abstinen. Periodica', default=False, blank=True)
    ant_mela = models.BooleanField('MELA', default=False, blank=True)
    ant_solo_ori_consej = models.BooleanField(
        'Solo Ori/Consej', default=False, blank=True)
    ant_condon = models.BooleanField('Condon', default=False, blank=True)
    ant_inyectables = models.BooleanField(
        'Progestag. Inyectables', default=False, blank=True)
    ant_ninguno = models.BooleanField('Ninguno', default=False, blank=True)
    ant_diu = models.BooleanField('DIU', default=False, blank=True)
    ant_orales = models.BooleanField(
        'Progestag. Orales', default=False, blank=True)
    ant_otro = models.BooleanField('Otro', default=False, blank=True)
    ant_observaciones = models.TextField(
        verbose_name='Observación', blank=True, null=True)

    cui = models.BooleanField('CUI', blank=False, default=False)
    seguro = models.BooleanField('Seguro', blank=False, default=False)

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='egreso_gestante_c')
    modifier = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='egreso_gestante_m')

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def save(self, *args, **kwargs):
        if self.diagnostico is not None:
            self.diagnostico_str = self.diagnostico.nombre_display
        if self.diagnostico_traslado is not None:
            self.diagnostico_traslado_str = self.diagnostico_traslado.nombre_display
        if self.diagnostico_fallecimiento is not None:
            self.diagnostico_fallecimiento_str = self.diagnostico_fallecimiento.nombre_display
        super(EgresoGestante, self).save(*args, **kwargs)


class EgresoRecienNacido(models.Model):

    TIPO_EGRESO_CHOICES = (
        ('sano', 'Sano'),
        ('traslado', 'Traslado'),
        ('con patologia', 'Con patologia'),
        ('fallece', 'Fallece')
    )

    SI_NO_CHOICES = (
        (True, 'Si'),
        (False, 'No')
    )

    recien_nacido = models.OneToOneField('RecienNacido', related_name='egreso')
    establecimiento = models.ForeignKey(
        'establecimientos.Establecimiento', related_name='egreso_establecimiento')
    diagnostico = models.ForeignKey(
        'cie.ICD10Base', related_name='egreso_diagnostico')
    diagnostico_traslado = models.ForeignKey(
        'cie.ICD10Base', related_name='egreso_diagnostico_traslado', blank=True, null=True)
    diagnostico_fallecimiento = models.ForeignKey(
        'cie.ICD10Base', related_name='egreso_diagnostico_fallecimiento', blank=True, null=True)

    diagnostico_str = models.CharField(
        max_length=255, editable=False, null=True)
    diagnostico_traslado_str = models.CharField(
        max_length=255, editable=False, null=True)
    diagnostico_fallecimiento_str = models.CharField(
        max_length=255, editable=False, null=True)

    fecha = models.DateField('Fecha')
    hora = models.TimeField('Hora')
    tipo = models.CharField(
        'Egreso', max_length=20, choices=TIPO_EGRESO_CHOICES, blank=False, null=False)
    establecimiento_traslado = models.CharField(
        'Establecimiento traslado', max_length=50, blank=True, null=True)

    peso = models.FloatField('Peso', default=0)
    cui = models.BooleanField('CUI', blank=False, default=False)
    seguro = models.BooleanField('Seguro', blank=False, default=False)

    # TN: tamizaje neonatal
    tn_tsh = models.BooleanField('TSH', blank=False, default=False)
    tn_fibrosis = models.BooleanField(
        'Fibrosis Quistica', blank=False, default=False)
    tn_fenilceto = models.BooleanField(
        'Fenilceto nuria', blank=False, default=False)
    tn_hiperplasia = models.BooleanField(
        'Hiperplasia Suprarrenal', blank=False, default=False)

    alimento_al_alta_lme = models.BooleanField(
        'LME', default=False, blank=True)
    alimento_al_alta_artificial = models.BooleanField(
        'Artificial', default=False, blank=True)
    alimento_al_alta_mixto = models.BooleanField(
        'Mixto', default=False, blank=True)
    alimento_al_alta_no_aplica = models.BooleanField(
        'No aplica', default=False, blank=True)

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='egresos_c')
    modifier = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='egresos_m')

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def save(self, *args, **kwargs):
        if self.diagnostico is not None:
            self.diagnostico_str = self.diagnostico.nombre_display
        if self.diagnostico_traslado is not None:
            self.diagnostico_traslado_str = self.diagnostico_traslado.nombre_display
        if self.diagnostico_fallecimiento is not None:
            self.diagnostico_fallecimiento_str = self.diagnostico_fallecimiento.nombre_display
        super(EgresoRecienNacido, self).save(*args, **kwargs)


class TerminacionPuerpera(models.Model):

    TIPO_EGRESO_CHOICES = (
        ('sano', 'Sano'),
        ('traslado', 'Traslado'),
        ('con patologia', 'Con patologia'),
        ('fallece', 'Fallece')
    )

    establecimiento = models.ForeignKey(
        'establecimientos.Establecimiento', related_name='terminacion_puerpera_establecimiento')
    paciente = models.ForeignKey('pacientes.Paciente', related_name='terminacion_puerpera_egresos')
    ingreso = models.OneToOneField('partos.Ingreso', related_name='terminacion_puerpera_gestante')
    terminacion_embarazo = models.OneToOneField(
        'partos.TerminacionEmbarazo', related_name='terminacion_puerpera_gestante')
    monitoreo = models.ForeignKey('puerperio.Monitoreo', related_name='monitoreo')

    fecha = models.DateField('Fecha')
    hora = models.TimeField('Hora')
    tipo = models.CharField('Egreso', max_length=20, choices=TIPO_EGRESO_CHOICES, blank=False, null=False)

    # ANT: anticonceptivos
    ant_ligadura_tubaria = models.BooleanField('Ligadura Tubaria', default=False, blank=True)
    ant_anticoncec_combinada = models.BooleanField('Anticoncec. Combinada', default=False, blank=True)
    ant_abstinencia_periodica = models.BooleanField('Abstinen. Periodica', default=False, blank=True)
    ant_mela = models.BooleanField('MELA', default=False, blank=True)
    ant_solo_ori_consej = models.BooleanField('Solo Ori/Consej', default=False, blank=True)
    ant_condon = models.BooleanField('Condón', default=False, blank=True)
    ant_inyectables = models.BooleanField('Progestag. Inyectables', default=False, blank=True)
    ant_ninguno = models.BooleanField('Ninguno', default=False, blank=True)
    ant_diu = models.BooleanField('DIU', default=False, blank=True)
    ant_orales = models.BooleanField('Progestag. Orales', default=False, blank=True)
    ant_otro = models.BooleanField('Otro', default=False, blank=True)
    ant_observaciones = models.TextField(verbose_name='Observación', blank=True, null=True)
    # Cita
    control_puerperio = models.DateField('Control puerperio', blank=True, null=True)
    centro_salud = models.ForeignKey('establecimientos.Establecimiento', null=True, blank=True)

    cetficiado_nacido_vivo = models.NullBooleanField('Certificado de nacido vivo', default=None)
    certificado_nacido_vivo_numero = models.IntegerField('Número', blank=True, null=True)

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='terminacion_puerpera_c')
    modifier = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='terminacion_puerpera_m')

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

