# coding:utf-8
from django.core import exceptions
from django.core.validators import (
    MinValueValidator, MaxValueValidator, RegexValidator)
from django.db import models

from common.util import print_choices


class Ocupacion(models.Model):
    nombre = models.CharField(u'Nombre', max_length=100)
    activo = models.BooleanField(u'Activo', default=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = u'Ocupación'
        verbose_name_plural = u'Ocupaciones'

    def __unicode__(self):
        return self.nombre


class Estudio(models.Model):
    nombre = models.CharField(u'Nombre', max_length=100)
    activo = models.BooleanField(u'Activo', default=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = u'Estudio'
        verbose_name_plural = u'Estudios'

    def __unicode__(self):
        return self.nombre


class Etnia(models.Model):
    nombre = models.CharField(u'Nombre', max_length=200)
    codigo = models.CharField(u'Código', max_length=10)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = u'Etnia'
        verbose_name_plural = u'Etnias'

    def __unicode__(self):
        return self.nombre


def validate_hc_length(value):
    if len(str(value)) > 10:
        raise exceptions.ValidationError(
            u'El número de HC debe contener como máximo 10 caracteres')


class HistoriaClinica(models.Model):
    numero = models.CharField(max_length=20, validators=[validate_hc_length])
    establecimiento = models.ForeignKey(
        'establecimientos.Establecimiento', related_name='historias_clinicas')
    paciente = models.ForeignKey('Paciente', related_name='historias_clinicas')

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        unique_together = (
            ('establecimiento', 'numero', 'paciente'),
            ('establecimiento', 'numero'), ('establecimiento', 'paciente'))


CELULAR_REGEX = RegexValidator(
    r'^\d{9}$', u'Ingrese un número valido(9 digitos sin espacios)')


class Paciente(models.Model):
    DOCUMENTO_DNI = 'dni'
    DOCUMENTO_LE = 'le'
    DOCUMENTO_LM = 'lm'
    DOCUMENTO_BOLETA = 'boleta'
    DOCUMENTO_PARTIDANACIMIENTO = 'partidanacimiento'
    DOCUMENTO_CARNETIDENTIDAD = 'carnetidentidad'
    DOCUMENTO_BREVETE = 'brevete'
    DOCUMENTO_CE = 'ce'
    DOCUMENTO_PASAPORTE = 'pasaporte'
    DOCUMENTO_CARNETUNIVERSITARIO = 'carnetuniversitario'
    DNI_EXTRANJERO = 'nie'
    NO_ESPECIFICA = 'noespecifica'
    NO_TRAJO = 'notrajo'
    NO_TIENE = 'nodoc'

    DOCUMENTO_CHOICES = (
        (DOCUMENTO_DNI, u'DNI'),
        (DOCUMENTO_LE, u'LIBRETA ELECTORAL'),
        (DOCUMENTO_LM, u'LIBRETA MILITAR'),
        (DOCUMENTO_BOLETA, u'BOLETA DE INSCRIPCION'),
        (DOCUMENTO_PARTIDANACIMIENTO, u'PARTIDA DE NACIMIENTO'),
        (DOCUMENTO_CARNETIDENTIDAD, u'CARNET DE IDENTIDAD'),
        (DOCUMENTO_BREVETE, u'BREVETE'),
        (DOCUMENTO_CE, u'CE'),
        (DOCUMENTO_PASAPORTE, u'Pasaporte'),
        (DOCUMENTO_CARNETUNIVERSITARIO, u'CARNET UNIVERSITARIO'),
        (DNI_EXTRANJERO, u'DIE'),
        (NO_ESPECIFICA, u'SIN ESPECIFICACION'),
        (NO_TRAJO, u'NO TRAJO DOCUMENTO'),
        (NO_TIENE, u'Indocumentado'),
    )

    TIEMPO_ESTUDIO_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9)
    )

    EC_SOLTERA = 'soltera'
    EC_DIVORCIADA = 'divorciada'
    EC_CASADA = 'casada'
    EC_VIUDA = 'viuda'
    EC_CONVIVIENTE = 'conviviente'

    EC_CHOICES = (
        (EC_SOLTERA, u'Soltera'),
        (EC_CONVIVIENTE, u'Conviviente'),
        (EC_CASADA, u'Casada'),
        (EC_DIVORCIADA, u'Divorciada'),
        (EC_VIUDA, u'Viuda'),
    )

    PARENTESCO_PADRE = 'padre'
    PARENTESCO_MADRE = 'madre'
    PARENTESCO_PAREJA = 'pareja'
    PARENTESCO_TUTOR = 'tutor'
    PARENTESCO_OTRO = 'otro'
    PARENTESCO_NO_APLICA = 'no aplica'

    PARENTESCO_CHOICES = (
        (PARENTESCO_NO_APLICA, u'No aplica'),
        (PARENTESCO_PADRE, u'Padre'),
        (PARENTESCO_MADRE, u'Madre'),
        (PARENTESCO_PAREJA, u'Pareja'),
        (PARENTESCO_OTRO, u'Otro')
    )

    COMPONENTE_SUBSIDIADO = 'subsidiado'
    COMPONENTE_SEMI_SUBSIDIADO = 'semi subsidiado'
    COMPONENTE_NO_APLICA = 'no aplica'

    COMPONENTE_CHOICES = (
        (COMPONENTE_NO_APLICA, u'No Aplica'),
        (COMPONENTE_SUBSIDIADO, u'Subsidiado'),
        (COMPONENTE_SEMI_SUBSIDIADO, u'Semi Subsidiado')
    )

    AFILIACION_NUEVO = 'nuevo'
    AFILIACION_INSCRITO = 'inscrito'
    AFILIACION_AFILIADO = 'afiliado'
    AFILIACION_NO_APLICA = 'no aplica'

    AFILIACION_CHOICES = (
        (AFILIACION_NO_APLICA, u'No Aplica'),
        (AFILIACION_NUEVO, u'Nuevo'),
        (AFILIACION_INSCRITO, u'Inscrito'),
        (AFILIACION_AFILIADO, u'Afiliado')
    )

    OPERADOR_BITEL = 'bitel'
    OPERADOR_CLARO = 'claro'
    OPERADOR_MOVISTAR = 'movistar'
    OPERADOR_ENTEL = 'entel'

    OPERADOR_CHOICES = (
        (OPERADOR_MOVISTAR, u'Movistar'),
        (OPERADOR_CLARO, u'Claro'),
        (OPERADOR_ENTEL, u'Entel'),
        (OPERADOR_BITEL, u'Bitel'),
    )

    CATEGORIZACION_CHOICES = (
        ('anexo', 'Anexo'),
        ('asentamiento humano', 'Asentamiento Humano'),
        ('asociacion de vivienda', u'Asociación de vivienda'),
        ('barrio o cuartel', 'Barrio o cuartel'),
        ('campamento minero', 'Campamento minero'),
        ('caserio', 'Caserio'),
        ('ciudad', 'Ciudad'),
        ('centro poblado','Centro Poblado'),
        ('comunidad campesina', 'Comunidad campesina'),
        ('comunidad indigena', u'Comunidad Indígena'),
        ('conjunto habitacional', 'Conjunto Habitacional'),
        ('cooperativa agraria de produccion',
         u'Cooperativa agraria de producción'),
        ('cooperativa de vivienda', 'Cooperativa de vivienda'),
        ('pueblo joven', 'Pueblo Joven'),
        ('pueblo', 'Pueblo'),
        ('unidad agropecuaria', 'Unidad Agropecuaria'),
        ('urbanizacion', u'Urbanización'),
    )

    foto = models.ImageField(
        u'Foto', upload_to='fotos/%Y/%m/%d/', blank=True, null=True)
    nombres = models.CharField(u'Nombres', max_length=100)
    apellido_paterno = models.CharField(u'Apellido Paterno', max_length=50)
    apellido_materno = models.CharField(u'Apellido Materno', max_length=50)
    tipo_documento = models.CharField(
        u'Tipo Documento', default=DOCUMENTO_DNI, choices=DOCUMENTO_CHOICES,
        max_length=20)
    numero_documento = models.CharField(max_length=20, blank=True, null=True)
    codigo = models.CharField(max_length=20, editable=False, null=True)
    dni_responsable = models.IntegerField(
        u'DNI del responsable', null=True, blank=True)
    nombre_responsable = models.CharField(
        u'Nombre del responsable', max_length=70, null=True, blank=True)
    responsable_otros = models.CharField(
        u'Otros', max_length=100, null=True, blank=True)
    fecha_nacimiento = models.DateField(u'Fecha de nacimiento')
    transfusion_sanguinea = models.NullBooleanField(
        u'Tranfusion sanguinea', default=None)
    tipo_parentesco_responsable = models.CharField(
        u'Tipo de parentesco', choices=PARENTESCO_CHOICES,
        default=PARENTESCO_NO_APLICA, max_length=10)

    pais_residencia = models.ForeignKey(
        'ubigeo.Pais', related_name='residencia_pacientes')
    departamento_residencia = models.ForeignKey('ubigeo.Departamento', related_name='residencia_pacientes', null=True)
    provincia_residencia = models.ForeignKey('ubigeo.Provincia', related_name='residencia_pacientes', null=True)
    distrito_residencia = models.ForeignKey('ubigeo.Distrito', related_name='residencia_pacientes', null=True)
    direccion = models.CharField(u'Dirección', max_length=100)
    categorizacion = models.CharField(
        u'Categorización', max_length=50, choices=CATEGORIZACION_CHOICES,
        null=True)
    urbanizacion = models.CharField(
        u'Sector', max_length=100, blank=True, null=True)
    direccion_completa = models.CharField(max_length=255)
    telefono = models.IntegerField(u'Teléfono de casa', blank=True, null=True)
    celular = models.CharField(
        u'Celular 1', max_length=10, blank=True, null=True,
        validators=[CELULAR_REGEX])
    celular2 = models.CharField(
        u'Celular 2', max_length=10, blank=True, null=True,
        validators=[CELULAR_REGEX])
    email = models.EmailField(
        u'Correo electronico', max_length=70, blank=True, null=True)

    pais_nacimiento = models.ForeignKey(
        'ubigeo.Pais', related_name='nacimiento_pacientes')
    departamento_nacimiento = models.ForeignKey(
        'ubigeo.Departamento', related_name='nacimiento_pacientes', null=True,
        blank=True)
    provincia_nacimiento = models.ForeignKey(
        'ubigeo.Provincia', related_name='nacimiento_pacientes', null=True,
        blank=True)

    estudio = models.ForeignKey(Estudio, null=True)
    estudio_nombre = models.CharField(max_length=100, blank=True, default='')
    tiempo_estudio = models.SmallIntegerField(
        u'Años aprobados', choices=TIEMPO_ESTUDIO_CHOICES, null=True)
    ocupacion = models.ForeignKey(Ocupacion, null=True)
    ocupacion_nombre = models.CharField(max_length=100, blank=True, default='')
    estado_civil = models.CharField(
        u'Estado Civil', choices=EC_CHOICES, max_length=20, null=True)
    etnia = models.ForeignKey(Etnia, null=True)
    etnia_nombre = models.CharField(max_length=100, blank=True, default='')

    seguro_sis = models.BooleanField(u'SIS', default=False, blank=True)
    seguro_essalud = models.BooleanField(u'Essalud', default=False)
    seguro_privado = models.BooleanField(u'Privado', default=False)
    seguro_sanidad = models.BooleanField(u'Sanidad', default=False)
    seguro_otros = models.BooleanField(u'Otros', default=False)
    codigo_afiliacion = models.CharField(
        u'Código afilicación', max_length=10, blank=True)

    componente = models.CharField(
        u'Componente', choices=COMPONENTE_CHOICES,
        default=COMPONENTE_NO_APLICA, max_length=20)
    afiliacion = models.CharField(
        u'Afiliacion', choices=AFILIACION_CHOICES,
        default=AFILIACION_NO_APLICA, max_length=20)

    antecedentes_familiares_niega = models.BooleanField(default=True)
    antecedentes_medicos_niega = models.BooleanField(default=True)

    recibir_sms = models.NullBooleanField(u'Recibir SMS', default=None)
    celular_wawared = models.IntegerField(
        u'Celular Wawared', null=True, blank=True)
    operador = models.CharField(
        u'Compañia Celular', choices=OPERADOR_CHOICES,
        default=OPERADOR_MOVISTAR, max_length=10)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    origen_phr = models.BooleanField(u'Phr', default=False)

    class Meta:
        verbose_name = u'Paciente'
        verbose_name_plural = u'Pacientes'
        unique_together = (
            'tipo_documento', 'numero_documento', 'dni_responsable')

    def __unicode__(self):
        return u'{nombre_completo}'.format(
            nombre_completo=self.nombre_completo)

    @property
    def get_estado_ultimo_partograma(self):
        from django.db.models import get_model
        Partograma = get_model('partos', 'Partograma')
        partograma = Partograma.objects.filter(paciente_id=self.id).last()
        return partograma.status if partograma else None

    @property
    def nombre_completo(self):
        return u'{nombres} {a_paterno} {a_materno}'.format(
            nombres=self.nombres,
            a_paterno=self.apellido_paterno,
            a_materno=self.apellido_materno
        )

    @property
    def nombre_documento(self):
        for choice in self.DOCUMENTO_CHOICES:
            if self.tipo_documento in choice:
                return choice[1]
        return ''

    @property
    def edad(self):
        from datetime import date
        today = date.today()
        try:
            birthday = self.fecha_nacimiento.replace(year=today.year)
        except ValueError:
            birthday = self.fecha_nacimiento.replace(
                year=today.year, day=self.fecha_nacimiento.day - 1)
        age = today.year - self.fecha_nacimiento.year
        if birthday > today:
            age -= 1
        return age

    def get_embarazo_actual(self):
        from django.db.models import get_model
        Embarazo = get_model('embarazos', 'Embarazo')
        try:
            embarazo = Embarazo.objects.get(paciente=self, activo=True)
            return embarazo
        except Exception:
            return None

    def tiene_seguro(self):

        if self.seguro_sis:
            return True

        return False

    def get_ultimo_atencion_embarazo_activo(self):
        from django.db.models import get_model

        Control = get_model('controles', 'Control')
        try:

            embarazo_activo = self.get_embarazo_actual()

            if embarazo_activo:
                atenciones = Control.objects.filter(embarazo_id=embarazo_activo.id).order_by('-atencion_fecha')[:1]

                if len(atenciones.values()) == 1:
                    atencion = atenciones[0]
                    return atencion

                return None
            else:
                return None
        except Exception as e:
            return None

    def generar_codigo(self):
        document_code = ''
        if self.tipo_documento == self.DOCUMENTO_DNI:
            document_code = '1'
        elif self.tipo_documento == self.DOCUMENTO_PASAPORTE:
            document_code = '3'
        elif self.tipo_documento == self.DOCUMENTO_CE:
            document_code = '2'
        # TODO: falta considerar cuando la paciente es menor sin documento
        self.codigo = '{}{}00'.format(document_code, self.numero_documento)

    def save(self, *args, **kwargs):
        if self.etnia is not None:
            self.etnia_nombre = self.etnia.nombre
        else:
            self.etnia_nombre = ''

        if self.estudio is not None:
            self.estudio_nombre = self.estudio.nombre
        else:
            self.estudio_nombre = ''

        if self.ocupacion is not None:
            self.ocupacion_nombre = self.ocupacion.nombre
        else:
            self.ocupacion_nombre = ''

        self.direccion_completa = u'{}-{}'.format(
            self.direccion, self.urbanizacion)
        self.generar_codigo()
        if not self.seguro_sis:
            self.codigo_afiliacion = ''
            self.componente = self.COMPONENTE_NO_APLICA
            self.afiliacion = self.AFILIACION_NO_APLICA
        super(Paciente, self).save(*args, **kwargs)
        if not hasattr(self, 'antecedente_obstetrico'):
            AntecedenteObstetrico.objects.create(paciente=self)
        if not hasattr(self, 'antecedente_ginecologico'):
            AntecedenteGinecologico.objects.create(paciente=self)

    def wawacel(self):
        """
        Se calcula a partir de los dos celulares cargados, si
        ya se selecciono uno para mensajes, se selecciona ese
        """
        cel = str(self.celular_wawared)
        if cel is None:
            cel = self.celular
        if cel is None:
            cel = self.celular2

        return cel


class AntecedenteGinecologico(models.Model):
    PAPANICOLAOU_RESULTADO_NO_APLICA = 'no aplica'
    PAPANICOLAOU_RESULTADO_NORMAL = 'normal'
    PAPANICOLAOU_RESULTADO_ANORMAL = 'anormal'

    PAPANICOLAOU_RESULTADO_CHOICES = (
        (PAPANICOLAOU_RESULTADO_NO_APLICA, u'N/A'),
        (PAPANICOLAOU_RESULTADO_NORMAL, u'Normal'),
        (PAPANICOLAOU_RESULTADO_ANORMAL, u'Anormal')
    )

    paciente = models.OneToOneField(
        'Paciente', related_name='antecedente_ginecologico')
    # papanicolaou
    tiene_papanicolaou = models.NullBooleanField(
        u'Tiene Papanicolaou', default=None)
    fecha_ultimo_papanicolaou = models.DateField(null=True, blank=True)
    resultado_papanicolaou = models.CharField(
        u'Resultado Papanicolaou', choices=PAPANICOLAOU_RESULTADO_CHOICES,
        default=PAPANICOLAOU_RESULTADO_NO_APLICA, max_length=20)
    lugar_papanicolaou = models.CharField(
        u'Lugar Papanicolaou', max_length=100, null=True, blank=True)
    pap_observacion = models.CharField(
        u'Observación', max_length=255, null=True, blank=True)
    # metodos anticonceptivos
    condon = models.BooleanField(u'Condon', default=False)
    ovulos = models.BooleanField(u'Ovulos', default=False)
    diu = models.BooleanField(u'DIU', default=False)
    inyectable = models.BooleanField(u'Inyectable 1 mes', default=False)
    inyectable_2 = models.BooleanField(u'Inyectable 3 meses', default=False)
    pastilla = models.BooleanField(u'Pastilla', default=False)
    implanon = models.BooleanField(u'Implanon', default=False)
    natural = models.BooleanField(u'Natural', default=False)

    embarazo_mac = models.NullBooleanField(
        u'Embarazo usando MAC', default=None)
    edad_menarquia = models.SmallIntegerField(
        u'Menarquia edad', default=None, null=True, blank=True,
        validators=[MinValueValidator(8), MaxValueValidator(20)])
    andria = models.SmallIntegerField(u'Andria', default=None, validators=[
        MinValueValidator(1), MaxValueValidator(99)], null=True, blank=True)
    edad_primera_relacion_sexual = models.SmallIntegerField(
        u'Edad primera relacion sexual', null=True, blank=True, default=None)
    regimen_regular = models.BooleanField(u'Regimen Regular', default=True)
    duracion_menstruacion = models.SmallIntegerField(
        u'Duración del ciclo menstrual', null=True, default=None, blank=True)
    ciclo_menstruacion = models.SmallIntegerField(
        null=True, default=None, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = u'Antecedente Ginecológico'
        verbose_name_plural = u'Antecedente Ginecológicos'

    print_resultado_papanicolaou = print_choices(
        'resultado_papanicolaou', PAPANICOLAOU_RESULTADO_CHOICES)

    def save(
        self, force_insert=False, force_update=False, using=None,
        update_fields=None):
        if not self.regimen_regular:
            self.duracion_menstruacion = 0
            self.ciclo_menstruacion = 0
        super(AntecedenteGinecologico, self).save(
            force_insert, force_update, using, update_fields)


class AntecedenteObstetrico(models.Model):
    paciente = models.OneToOneField(
        'Paciente', related_name='antecedente_obstetrico')
    gestaciones = models.PositiveSmallIntegerField(default=0)
    abortos = models.PositiveSmallIntegerField(default=0)
    partos = models.PositiveSmallIntegerField(default=0)
    cesareas = models.PositiveSmallIntegerField(
        u'Cesáreas', default=0, blank=True, null=True)
    vaginales = models.PositiveSmallIntegerField(
        u'Vaginales', default=0, blank=True, null=True)
    rn_mayor_peso = models.SmallIntegerField(default=0, blank=True, null=True)
    nacidos_vivos = models.SmallIntegerField(default=0)
    nacidos_muertos = models.SmallIntegerField(default=0)
    viven = models.SmallIntegerField(default=0)
    muertos_menor_una_sem = models.SmallIntegerField(default=0)
    muertos_mayor_igual_1sem = models.SmallIntegerField(default=0)
    obitos = models.SmallIntegerField(default=0, blank=True, null=True)
    primigesta = models.BooleanField(default=False)
    nacidos_menor_2500g = models.SmallIntegerField(
        default=0, blank=True, null=True)
    nacidos_menor_37sem = models.SmallIntegerField(
        default=0, blank=True, null=True)
    preeclampsias = models.SmallIntegerField(default=0, blank=True, null=True)
    hemorragias_postparto = models.SmallIntegerField(
        default=0, blank=True, null=True)
    embarazos_multiples = models.SmallIntegerField(
        default=0, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def reset(self):
        self.gestaciones = 0
        self.abortos = 0
        self.partos = 0
        self.cesareas = 0
        self.vaginales = 0
        self.rn_mayor_peso = 0
        self.nacidos_menor_2500g = 0
        self.nacidos_menor_37sem = 0
        self.viven = 0
        self.nacidos_vivos = 0
        self.nacidos_muertos = 0
        self.muertos_mayor_igual_1sem = 0
        self.muertos_menor_una_sem = 0
        self.obitos = 0
        self.embarazos_multiples = 0
        self.save()

    def generate(self):
        from embarazos.models import UltimoEmbarazo, Bebe
        self.reset()
        vivos = 0
        muertos_men_1_semana = 0
        muertos_may_1_semana = 0
        muertos = 0
        for embarazo in self.paciente.ultimos_embarazos.all():
            self.gestaciones += 1
            if embarazo.tipo == UltimoEmbarazo.TIPO_MULTIPLE:
                self.embarazos_multiples += 1

            for bebe in embarazo.bebes.all().distinct():
                if bebe.terminacion == Bebe.TERMINACION_VAGINAL:
                    self.vaginales += 1
                elif bebe.terminacion == Bebe.TERMINACION_OBITO:
                    self.vaginales += 1
                    self.obitos += 1
                elif bebe.terminacion in (
                    Bebe.TERMINACION_ABORTO,
                    Bebe.TERMINACION_ABORTO_MOLAR,
                    Bebe.TERMINACION_ECTOPICO):
                    self.abortos += 1

            for bebe in embarazo.bebes.all():
                if bebe.peso and self.rn_mayor_peso < bebe.peso:
                    self.rn_mayor_peso = bebe.peso
                if bebe.terminacion in (
                    Bebe.TERMINACION_CESAREA, Bebe.TERMINACION_CESAREA) \
                    and bebe.edad_gestacional < 37:
                    self.nacidos_menor_37sem += 1
                if bebe.terminacion in (
                    Bebe.TERMINACION_CESAREA, Bebe.TERMINACION_CESAREA) \
                    and bebe.peso < 2500:
                    self.nacidos_menor_2500g += 1
                if bebe.vive:
                    self.viven += 1
                if bebe.muerte == Bebe.MUERTE_NACIO_MUERTO:
                    self.nacidos_muertos += 1
                elif bebe.muerte == Bebe.MUERTE_MENOR_PRIMERA_SEMANA:
                    self.muertos_menor_una_sem += 1
                elif bebe.muerte == Bebe.MUERTE_MAYOR_PRIMERA_SEMANA:
                    self.muertos_mayor_igual_1sem += 1

            for bebe in embarazo.bebes.all().distinct('fecha'):
                if bebe.terminacion == Bebe.TERMINACION_CESAREA:
                    self.cesareas += 1
                if bebe.vive:
                    vivos += 1
                if bebe.muerte == Bebe.MUERTE_NACIO_MUERTO:
                    muertos += 1
                elif bebe.muerte == Bebe.MUERTE_MENOR_PRIMERA_SEMANA:
                    muertos_men_1_semana += 1
                elif bebe.muerte == Bebe.MUERTE_MAYOR_PRIMERA_SEMANA:
                    muertos_may_1_semana += 1

        # self.partos = self.vaginales + self.cesareas + self.obitos
        self.nacidos_vivos = self.viven + self.muertos_menor_una_sem
        self.nacidos_vivos += self.muertos_mayor_igual_1sem
        self.partos = vivos + muertos_men_1_semana + muertos_may_1_semana + muertos
        self.save()


class AntecedenteFamiliar(models.Model):
    paciente = models.ForeignKey(
        'Paciente', related_name='antecedentes_familiares')
    cie = models.ForeignKey('cie.ICD10')
    relaciones = models.ManyToManyField('RelacionParentesco', blank=True)
    observacion = models.TextField(u'Observacion', blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        unique_together = ('paciente', 'cie')
        ordering = ('cie__nombre_mostrar', 'cie__nombre')


class AntecedenteMedico(models.Model):
    paciente = models.ForeignKey(
        'Paciente', related_name='antecedentes_medicos')
    cie = models.ForeignKey('cie.ICD10Medical')
    observacion = models.TextField(u'Observacion', blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        unique_together = ('paciente', 'cie')
        ordering = ('cie__nombre_mostrar', 'cie__nombre')


class Vacuna(models.Model):
    paciente = models.OneToOneField(
        'pacientes.Paciente', related_name='vacuna')

    # Vacunas previas
    rubeola = models.NullBooleanField(u'Rubeola')
    hepatitis_b = models.NullBooleanField(u'Hepatitis B')
    papiloma = models.NullBooleanField(u'Papiloma')
    fiebre_amarilla = models.NullBooleanField(u'Fiebre amarilla')
    h1n1 = models.NullBooleanField(u'H1N1')
    influenza = models.NullBooleanField('Influenza')

    # Antitetanica
    antitetanica_numero_dosis_previas = models.SmallIntegerField(
        u'Numero dosis previas', default=0, blank=True, null=True)
    antitetanica_primera_dosis = models.NullBooleanField(
        u'Antitetanica primera dosis', default=None, blank=True, null=True)
    antitetanica_primera_dosis_valor = models.CharField(
        u'Antitetanica primera dosis valor', max_length=10, blank=True,
        null=True)
    antitetanica_segunda_dosis = models.NullBooleanField(
        u'Antitetanica segunda dosis', default=None, blank=True, null=True)
    antitetanica_segunda_dosis_valor = models.CharField(
        u'Antitetanica segunda dosis valor', max_length=10, blank=True,
        null=True)
    antitetanica_tercera_dosis = models.NullBooleanField(
        u'Antitetanica tercera dosis', default=None, blank=True, null=True)
    antitetanica_tercera_dosis_valor = models.CharField(
        u'Antitetanica tercera dosis valor', max_length=10, blank=True,
        null=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = u'Vacuna'
        verbose_name_plural = u'Vacunas'


class RelacionParentesco(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    solo_femenino = models.BooleanField(u'Solo femenino', default=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return self.nombre
