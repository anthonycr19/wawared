# coding: utf-8
from __future__ import unicode_literals
from datetime import datetime
from datetime import timedelta

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from controles.models import DESCENSO_CEFALICO_CHOICES, ExamenFisicoFetal


class Ingreso(models.Model):
    TIPO_PARTO = 'parto'
    TIPO_ABORTO = 'aborto'

    TIPO_CHOICES = (
        (TIPO_PARTO, 'Parto'),
        (TIPO_ABORTO, 'Aborto')
    )

    INICIO_ESPONTANEO = 'espontaneo'
    INICIO_INDUCIDO = 'inducido'

    INICIO_CHOICES = (
        (INICIO_ESPONTANEO, 'Espontáneo'),
        (INICIO_INDUCIDO, 'Inducido'),
    )

    EG_FUM = 'fum'
    EG_ECOGRAFIA = 'ecografia'
    EG_ALTURA_UTERINA = 'altura uterina'

    EG_CHOICES = (
        (EG_FUM, 'FUM'),
        (EG_ECOGRAFIA, 'Ecografía'),
        (EG_ALTURA_UTERINA, 'Altura Uterina')
    )

    OTROS = 'otros'

    LUGAR_DE_DERIVACION_SALA_DE_DILATACION = 'sala de dilatacion'
    LUGAR_DE_DERIVACION_SALA_DE_EXPULSION = 'sala de expulsion'
    LUGAR_DE_DERIVACION_DOMICILIO = 'domicilio'

    LUGAR_DE_DERIVACION_CHOICES = (
        (LUGAR_DE_DERIVACION_SALA_DE_DILATACION, 'Sala de dilatación'),
        (LUGAR_DE_DERIVACION_SALA_DE_EXPULSION, 'Sala de expulsión'),
        (LUGAR_DE_DERIVACION_DOMICILIO, 'Domicilio'),
        (OTROS, 'Otros')
    )

    establecimiento = models.ForeignKey(
        'establecimientos.Establecimiento',
        related_name='ingresos')
    paciente = models.ForeignKey('pacientes.Paciente', related_name='ingresos')
    embarazo = models.OneToOneField(
        'embarazos.Embarazo',
        related_name='ingreso')
    fecha = models.DateField('Fecha')
    hora = models.TimeField('Hora')
    tipo = models.CharField(
        'Tipo de ingreso',
        max_length=20,
        choices=TIPO_CHOICES,
        default=TIPO_PARTO)

    inicio = models.CharField(
        'Inicio',
        max_length=20,
        choices=INICIO_CHOICES,
        default=INICIO_ESPONTANEO)
    cama = models.SmallIntegerField('Cama', null=True, blank=True)
    visito_sintomas = models.BooleanField(default=False)
    asintomatica = models.BooleanField('Asintomática', default=False)
    eg_fum = models.CharField(
        'EG FUM',
        max_length=20,
        default=None,
        blank=True,
        null=True)
    eg_ecografia = models.CharField(
        'EG ecografía',
        max_length=20,
        default=None,
        blank=True,
        null=True)
    eg_altura_uterina = models.CharField(
        'EG altura uterina',
        max_length=20,
        default=None,
        blank=True,
        null=True)
    eg_elegida = models.CharField(
        'EG escogida',
        choices=EG_CHOICES,
        default=EG_FUM,
        max_length=20,
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
        MinValueValidator(20), MaxValueValidator(300)
    ])
    imc = models.FloatField('IMC')
    imc_clasificacion = models.CharField('IMC clasificacion', max_length=20, blank=True, null=True)
    temperatura = models.FloatField('Temperatura', null=True, blank=True, validators=[
        MinValueValidator(25), MaxValueValidator(50)])
    presion_sistolica = models.SmallIntegerField('Presion sistolica', null=True, blank=True, validators=[
        MinValueValidator(0), MaxValueValidator(300)])
    presion_diastolica = models.SmallIntegerField('Presion diastolica', null=True, blank=True, validators=[
        MinValueValidator(0), MaxValueValidator(200)])
    pulso = models.PositiveSmallIntegerField('Pulso', null=True, max_length=2, blank=True, validators=[
        MinValueValidator(0), MaxValueValidator(400)])
    frecuencia_respiratoria = models.SmallIntegerField('Frecuencia respiratoria', null=True, blank=True,
                                                       validators=[MinValueValidator(1), MaxValueValidator(180)])
    altura_uterina = models.SmallIntegerField(
        'Altura uterina', blank=True, null=True, validators=[MinValueValidator(5), MaxValueValidator(40)])
    situacion = models.CharField('Situacion', max_length=20, choices=(
        ('longitudinal', 'Longitudinal'),
        ('transversal', 'Transversal'),
        ('na', 'NA'),
    ), null=True, blank=True)
    presentacion = models.CharField('Presentacion', max_length=20, choices=(
        ('cefalico', 'Cefalico'),
        ('podalico', 'Podalico'),
        ('na', 'NA')
    ), null=True, blank=True)
    posicion = models.CharField('Posicion', max_length=20, choices=(
        ('derecho', 'Derecho'),
        ('izquierdo', 'Izquierdo'),
        ('na', 'NA')
    ), null=True, blank=True)
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
    edemas = models.CharField('Edemas', max_length=5, choices=(
        ('se', 'Sin Edemas'),
        ('+', '+'),
        ('++', '++'),
        ('+++', '+++'),
    ), null=True, blank=True)
    reflejos = models.CharField('Reflejos', max_length=20, choices=(
        ('0', '0'),
        ('+', '+'),
        ('++', '++'),
        ('+++', '+++'),
    ), null=True, blank=True)
    lugar_de_derivacion = models.CharField(
        'Lugar de derivación',
        max_length=30,
        choices=LUGAR_DE_DERIVACION_CHOICES,
        null=True,
        blank=True)
    lugar_de_derivacion_otros = models.CharField(
        'Otros', max_length=50, blank=True, null=True)

    atencion_fonp = models.BooleanField('FONP', default=False)
    atencion_fonb = models.BooleanField('FONB', default=False)
    atencion_foni = models.BooleanField('FONI', default=False)
    atencion_fone_1 = models.BooleanField('FONE I', default=False)
    atencion_fone_2 = models.BooleanField('FONE II', default=False)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    tiempo_ruptura_membranas_horas = models.IntegerField(
        'Tiempo horas', blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(48)])
    tiempo_ruptura_membranas_minutos = models.IntegerField(
        'Tiempo minutos', blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(60)])

    class Meta:
        ordering = ('fecha', 'hora')

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None):
        self.imc_clasificacion = self.get_imc_clasificacion()
        self.edad_gestacional_semanas = self.get_edad_gestacionl()
        super(Ingreso, self).save(force_insert, force_update, using, update_fields)

    @property
    def presion_arterial(self):
        return '{}/{}'.format(self.presion_sistolica, self.presion_diastolica)

    def get_imc_clasificacion(self):
        """función para clasificar el imc"""
        if self.imc < 19.8:
            return 'bajo peso'
        elif 19.8 <= self.imc <= 26:
            return 'normal'
        elif 26 < self.imc <= 29:
            return 'sobrepeso'
        else:
            return 'obesidad'

    def get_edad_gestacionl(self):
        """ función para guardar la edad gestacional elegida """
        eg_elegida = self.eg_elegida

        if eg_elegida == 'fum' and len(self.eg_fum) > 0:
            edad_gestacional_semanas = int(self.eg_fum.split()[0])
        elif eg_elegida == 'ecografia' and len(self.eg_ecografia) > 0:
            edad_gestacional_semanas = int(self.eg_ecografia.split()[0])
        elif eg_elegida == 'altura uterina' and len(self.eg_altura_uterina) > 0:
            edad_gestacional_semanas = int(self.eg_altura_uterina.split()[0])
        else:
            edad_gestacional_semanas = None

        return edad_gestacional_semanas


class Partograma(models.Model):

    """ Módelo para guardar los datos del partograma """
    ABIERTO = 'abierto'
    CERRADO = 'cerrado'

    establecimiento = models.ForeignKey(
        'establecimientos.Establecimiento',
        related_name='partogramas')
    paciente = models.ForeignKey(
        'pacientes.Paciente',
        related_name='partogramas')
    ingreso = models.OneToOneField('Ingreso', related_name='partograma')

    status = models.CharField(max_length=20, default=ABIERTO)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def get_fcfs(self, fcfs):
        fcf_string = ''
        for fcf_m in fcfs:
            fcf_string += str(fcf_m.fcf) + " "
        return fcf_string

    def get_mediciones_dict(self):
        data = {}

        mediciones = self.mediciones.all()
        first_medicion = mediciones.first()
        if not first_medicion:
            return dict((i, {}) for i in range(1, 25))
        initial_date = datetime.combine(
            first_medicion.fecha, first_medicion.hora)

        counter = 1
        for i in range(1, 25):
            init = initial_date.time()
            final = (initial_date + timedelta(minutes=30)).time()
            qs = mediciones.filter(hora__gte=init, hora__lt=final)
            presion_sistolica = 0
            presion_diastolica = 0
            temperatura = ''
            pulso = 0
            oxitocina = ''
            goteo = ''
            frecuencia = ''
            duracion = ''
            liquido_amniotico = ''
            dilatacion = ''
            descenso_cefalico = ''
            hora = ''
            fcf = 0
            moldeaminetos = ''
            orina_volumen = ''
            orina_cetona = ''
            orina_proteinas = ''

            if qs:
                obj = qs.first()
                presion_sistolica = obj.presion_sistolica
                presion_diastolica = obj.presion_diastolica
                temperatura = obj.temperatura
                pulso = obj.pulso
                oxitocina = obj.oxitocina
                goteo = obj.goteo
                frecuencia = obj.du_frecuencia
                duracion = obj.du_duracion
                liquido_amniotico = obj.get_liquido_amniotico_chart()
                fcf = self.get_fcfs(ExamenFisicoFetal.objects.filter(medicion_parto=qs))
                dilatacion = obj.tv_dilatacion
                descenso_cefalico = obj.tv_descenso_cefalico if obj.tv_descenso_cefalico else ''
                hora = obj.hora.strftime('%H:%M')
                moldeaminetos = obj.moldeaminetos or ''
                orina_volumen = obj.orina_volumen
                orina_cetona = obj.orina_cetona
                orina_proteinas = obj.orina_proteinas

            data[counter] = {
                'sistolica': presion_sistolica or 0,
                'diastolica': presion_diastolica or 0,
                'moldeaminetos': moldeaminetos,
                'pulso': pulso or 0,
                'temperatura': temperatura or '',
                'goteo': goteo,
                'oxitocina': oxitocina,
                'frecuencia': frecuencia,
                'duracion': duracion,
                'liquido_amniotico': liquido_amniotico,
                'fcf': fcf or 0,
                'dilatacion': dilatacion or '',
                'descenso_cefalico': int(descenso_cefalico) if descenso_cefalico.isdigit() else '',
                'hora': hora,
                'orina_volumen': orina_volumen,
                'orina_cetona': orina_cetona or '',
                'orina_proteinas': orina_proteinas or ''}
            initial_date += timedelta(minutes=30)
            counter += 1

        return data


class PartogramaMedicion(models.Model):
    MOLDEAMINETOS_CHOICES = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3')
    )

    partograma = models.ForeignKey('Partograma', related_name='mediciones')

    fecha = models.DateField('Fecha')
    hora = models.TimeField('Hora')

    soluciones = models.NullBooleanField('Soluciones', default=None)

    solucion = models.CharField('Solución', max_length=100, blank=True)
    tocolisis = models.CharField('Tocolisis', max_length=100, blank=True)
    oxitocina = models.CharField('Oxitocina', max_length=100, blank=True)
    goteo = models.CharField('Goteo', max_length=100, blank=True)

    medicamentos = models.TextField(verbose_name='Medicamentos', blank=True, null=True)

    orina_volumen = models.IntegerField('Volumen', null=True, blank=True, validators=[
        MinValueValidator(0), MaxValueValidator(9999)])
    orina_cetona = models.CharField('Cetonas', max_length=100, blank=True, null=True)
    orina_proteinas = models.CharField(
        'Proteínas', max_length=10, blank=True, choices=(
            ('+', '+'),
            ('++', '++'),
            ('+++', '+++')
        ))
    observaciones = models.TextField(verbose_name='Observaciones', blank=True, null=True)
    # Funciones vitales
    presion_sistolica = models.SmallIntegerField('Presion sistolica', null=True, blank=True, validators=[
            MinValueValidator(0), MaxValueValidator(300)])
    presion_diastolica = models.SmallIntegerField('Presion diastolica', null=True, blank=True, validators=[
            MinValueValidator(0), MaxValueValidator(200)])
    pulso = models.PositiveSmallIntegerField('Pulso', null=True, max_length=2, blank=True, validators=[
            MinValueValidator(0), MaxValueValidator(400)])
    frecuencia_respiratoria = models.SmallIntegerField('Frecuencia respiratoria', null=True, blank=True, validators=[
            MinValueValidator(1), MaxValueValidator(180)])
    temperatura = models.FloatField('Temperatura', null=True, blank=True, validators=[
            MinValueValidator(25), MaxValueValidator(50)])
    moldeaminetos = models.CharField('Moldeamientos', max_length=10, null=True, blank=True,
                                     choices=MOLDEAMINETOS_CHOICES)
    # Dinamica uterina
    du_frecuencia = models.CharField('Frecuencia', max_length=10, blank=True, choices=(
        ('1/10', '1/10'),
        ('2/10', '2/10'),
        ('3/10', '3/10'),
        ('4/10', '4/10'),
        ('5+/10', '5+/10'),
    ))
    du_duracion = models.CharField('Duración', max_length=20, blank=True, choices=(
        ('-20', 'menos de 20'), ('20 - 40', '20 a 40'), ('40+', '40 a mas')))
    du_intensidad = models.CharField('Intensidad', max_length=10, blank=True, choices=(
            ('+', '+'), ('++', '++'), ('+++', '+++')))
    # Feto
    fcf = models.SmallIntegerField('FCF', blank=True, null=True, max_length=3, validators=[
            MinValueValidator(120), MaxValueValidator(400)])
    # Tacto vaginal
    tv_dilatacion = models.SmallIntegerField('Dilatación', blank=True, null=True, choices=(
            (n, str(n)) for n in range(0, 11)
            ))
    tv_incorporacion = models.CharField('Incorporación', max_length=20, blank=True, choices=(
        ('-40%', 'menos de 40%'),
        ('50%', '50%'),
        ('70%', '70%'),
        ('80%', '80%'),
        ('90%', '90%'),
        ('100%', '100%'),
    ))
    tv_descenso_cefalico = models.CharField(
        'Descenso cefálico',
        max_length=5,
        blank=True,
        null=True,
        choices=DESCENSO_CEFALICO_CHOICES)
    tv_membranas = models.CharField('Membranas', max_length=10, choices=(
        ('integras', 'Íntegras'),
        ('rotas', 'Rotas')
    ), blank=True)
    tv_membranas_rotas_tipo = models.CharField('Tipo', max_length=10, choices=(
        ('artificial', 'Artificial'),
        ('espontanea', 'Espontanea')
    ), blank=True)
    tv_membranas_rotas_tiempo = models.FloatField('Tiempo', null=True, blank=True, validators=[
            MinValueValidator(0), MaxValueValidator(48)])
    tv_liquido_amniotico = models.CharField('Líquido amniótico', max_length=20, choices=(
            ('claro', 'Claro'),
            ('meconial', 'Meconial'),
            ('sanguinolento', 'Sanguinolento')
            ), blank=True, null=True)

    tv_variedad_presentacion_val1 = models.CharField(max_length=20, choices=(
        ('anterior', 'Anterior'),
        ('transverso', 'Transverso'),
        ('posterior', 'Posterior')
    ), null=True, blank=True)

    tv_variedad_presentacion_val2 = models.CharField(max_length=20, choices=(
        ('derecho', 'Derecho'),
        ('izquierdo', 'Izquierdo'),
        ('no aplica', 'No aplica')
    ), null=True, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ('fecha', 'hora')

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None):
        if not self.soluciones:
            self.solucion = ''
            self.tocolisis = ''
            self.oxitocina = ''
            self.goteo = ''
        if self.tv_membranas == 'integras':
            self.tv_membranas_rotas_tipo = ''
            self.tv_liquido_amniotico = ''
        super(
            PartogramaMedicion,
            self).save(
                force_insert,
                force_update,
                using,
                update_fields)

    @property
    def variedad_presentacion(self):
        if self.tv_variedad_presentacion_val1 and self.tv_variedad_presentacion_val2:
            return 'O{}{}'.format(self.tv_variedad_presentacion_val1[:1],
                                  self.tv_variedad_presentacion_val2[:1]).upper()
        return ''

    @property
    def presion_arterial(self):
        if self.presion_sistolica and self.presion_diastolica:
            return '{}/{}'.format(self.presion_sistolica,
                                  self.presion_diastolica)
        return ''

    def get_liquido_amniotico_chart(self):
        if self.tv_membranas == 'integras':
            return 'I'
        if self.tv_membranas == 'rotas':
            if self.tv_liquido_amniotico:
                if self.tv_liquido_amniotico == 'claro':
                    return 'C'
                elif self.tv_liquido_amniotico == 'meconial':
                    return 'M'
                elif self.tv_liquido_amniotico == 'sanguinolento':
                    return 'S'
            else:
                return 'R'
        return ''


class TerminacionEmbarazo(models.Model):
    TIPO_UNICO = 'unico'
    TIPO_MULTIPLE = 'multiple'

    TIPO_CHOICES = (
        (TIPO_UNICO, 'Único'),
        (TIPO_MULTIPLE, 'Múltiple')
    )

    PARTO_ESPONTANEO = 'parto espontaneo'
    FORCEPS = 'forceps'
    VACUUM = 'vacuum'
    CESAREA_ELECTIVA = 'cesarea electiva'
    CESAREA_EMERGENCIA = 'cesarea emergencia'

    TERMINACION_CHOICES = (
        (PARTO_ESPONTANEO, 'Parto espontaneo'),
        (FORCEPS, 'Forces'),
        (VACUUM, 'Vacuum'),
        (CESAREA_ELECTIVA, 'Cesárea electiva'),
        (CESAREA_EMERGENCIA, 'Cesárea emergencia')
    )

    NO_APLICA = 'no aplica'

    PROCEDIMIENTO_CORPORAL = 'corporal'
    PROCEDIMIENTO_SEGMENTARIA = 'segmentaria'

    PROCEDIMIENTO_CHOICES = (
        (PROCEDIMIENTO_CORPORAL, 'Corporal'),
        (PROCEDIMIENTO_SEGMENTARIA, 'Segmentaria'),
        (NO_APLICA, 'No aplica')
    )

    POSICION_VERTICAL = 'vertical'
    POSICION_HORIZONTAL = 'horizontal'

    POSICION_CHOICES = (
        (POSICION_VERTICAL, 'Vertical'),
        (POSICION_HORIZONTAL, 'Horizontal'),
        (NO_APLICA, 'No aplica')
    )

    DURACION_NORMAL = 'normal'
    DURACION_PROLONGADO = 'prolongado'
    DURACION_PRECIPITADO = 'precipitado'

    DURACION_CHOICES = (
        (DURACION_NORMAL, 'Normal'),
        (DURACION_PROLONGADO, 'Prolongado'),
        (DURACION_PRECIPITADO, 'Precipitado'),
        (NO_APLICA, 'No aplica')
    )

    NO_HUBO = 'no hubo'
    MUERTE_INTRAUTERINA_DURANTE_EMBARAZO = 'durante embarazo'
    MUERTE_INTRAUTERINA_DURANTE_PARTO = 'durante parto'
    MUERTE_INTRAUTERINA_MOMENTO_DESCONOCIDO = 'momento desconocido'

    MUERTE_INTRAUTERINA_CHOICES = (
        (NO_HUBO, 'No hubo'),
        (MUERTE_INTRAUTERINA_DURANTE_EMBARAZO, 'Durante embarazo'),
        (MUERTE_INTRAUTERINA_DURANTE_PARTO, 'Durante parto'),
        (MUERTE_INTRAUTERINA_MOMENTO_DESCONOCIDO, 'Momento desconocido')
    )

    DESGARRO_GRADO_I = '1'
    DESGARRO_GRADO_II = '2'
    DESGARRO_GRADO_III_IV = '3'
    DESGARRO_GRADO_IV = '4'

    DESGARROS_CHOICES = (
        (DESGARRO_GRADO_I, '1'),
        (DESGARRO_GRADO_II, '2'),
        (DESGARRO_GRADO_III_IV, '3'),
        (DESGARRO_GRADO_IV, '4'),
    )

    ALUMBRAMIENTO_ACTIVO = 'activo'
    ALUMBRAMIENTO_EXPONTANEO = 'expontaneo'
    ALUMBRAMIENTO_MANUAL = 'manual'

    ALUMBRAMIENTO_CHOICES = (
        (ALUMBRAMIENTO_ACTIVO, 'Activo'),
        (ALUMBRAMIENTO_EXPONTANEO, 'Expontaneo'),
        (ALUMBRAMIENTO_MANUAL, 'Manual')
    )

    PLACENTA_COMPLETA = 'completa'
    PLACENTA_IMCOMPLETA = 'imcompleta'
    PLACENTA_RETENIDA = 'retenida'

    PLACENTA_CHOICES = (
        (PLACENTA_COMPLETA, 'Completa'),
        (PLACENTA_IMCOMPLETA, 'Incompleta'),
        (PLACENTA_RETENIDA, 'Retenida')
    )

    LIGADURA_CORDON_PRECOZ = 'precoz'
    LIGADURA_CORDON_TEMPRANA = 'temprana'
    LIGADURA_CORDON_TARDIA = 'tardia'

    LIGADURA_CORDON_CHOICES = (
        (LIGADURA_CORDON_PRECOZ, 'Precoz'),
        (LIGADURA_CORDON_TEMPRANA, 'Temprana'),
        (LIGADURA_CORDON_TARDIA, 'Tardía')
    )

    CORDON_UMBILICAL_NORMAL = 'normal'
    CORDON_UMBILICAL_VASOS_INCOMPLETOS = 'vasos incompletos'
    CORDON_UMBILICAL_CORTO = 'corto'
    CORDON_UMBILICAL_CIRCULAR_SIMPLE = 'circular simple'
    CORDON_UMBILICAL_CIRCULAR_DOBLE = 'circular doble'

    CORDON_UMBILICAL_CHOICES = (
        (CORDON_UMBILICAL_NORMAL, 'Normal'),
        (CORDON_UMBILICAL_VASOS_INCOMPLETOS, 'Vasos Incompletos'),
        (CORDON_UMBILICAL_CORTO, 'Corto'),
        (CORDON_UMBILICAL_CIRCULAR_SIMPLE, 'Circular Simple'),
        (CORDON_UMBILICAL_CIRCULAR_DOBLE, 'Circular Doble')
    )

    ESPONTANEO = 'espontaneo'
    INDUCIDO = 'inducido'
    ESTIMULADO = 'estimulado'

    LISTADO_CHOICES = (
        (ESPONTANEO, 'Espontaneo'),
        (INDUCIDO, 'Inducido'),
        (ESTIMULADO, 'Estimulado')
    )

    SI = 's'
    NO = 'n'

    BOOLEAN_CHOICES = (
        (SI, 'Si'),
        (NO, 'No')
    )

    TIPO_EPISIOTOMIA_M = 'M'
    TIPO_EPISIOTOMIA_MLD = 'MLD'
    TIPO_EPISIOTOMIA_MLI = 'MLI'

    TIPO_EPISIOTOMIA_CHOICES = (
        (TIPO_EPISIOTOMIA_M, 'M'),
        (TIPO_EPISIOTOMIA_MLD, 'MLD'),
        (TIPO_EPISIOTOMIA_MLI, 'MLI')
    )

    tipo = models.CharField(max_length=20, default=TIPO_UNICO, choices=TIPO_CHOICES, blank=True, null=True)
    fecha = models.DateField('Fecha', default=None, blank=True, null=True)
    hora = models.TimeField('Hora', default=None, blank=True, null=True)

    duracion_parto_perdiodo_1_horas = models.IntegerField('1er periodo', blank=True, null=True, validators=[
            MinValueValidator(0), MaxValueValidator(48)])
    duracion_parto_perdiodo_1_minutos = models.IntegerField('', blank=True, null=True, validators=[
            MinValueValidator(0), MaxValueValidator(60)])
    inicio_parto_periodo_1 = models.CharField('Inicio', max_length=20, choices=LISTADO_CHOICES, blank=True, null=True)
    duracion_parto_perdiodo_2_horas = models.IntegerField('2do periodo', blank=True, null=True, validators=[
            MinValueValidator(0), MaxValueValidator(48)])
    duracion_parto_perdiodo_2_minutos = models.IntegerField('', blank=True, null=True, validators=[
            MinValueValidator(0), MaxValueValidator(60)])
    inicio_parto_periodo_2 = models.CharField('Inicio', max_length=20, choices=LISTADO_CHOICES, blank=True, null=True)
    hora_1_parto_periodo_2 = models.TimeField('Hora', blank=True, null=True)
    hora_2_parto_periodo_2 = models.TimeField('Hora 2', blank=True, null=True)
    hora_3_parto_periodo_2 = models.TimeField('Hora 3', blank=True, null=True)
    hora_4_parto_periodo_2 = models.TimeField('Hora 4', blank=True, null=True)
    hora_5_parto_periodo_2 = models.TimeField('Hora 5', blank=True, null=True)
    duracion_parto_perdiodo_3_horas = models.IntegerField('3er periodo', blank=True, null=True, validators=[
            MinValueValidator(0), MaxValueValidator(48)])
    duracion_parto_perdiodo_3_minutos = models.IntegerField('', blank=True, null=True, validators=[
            MinValueValidator(0), MaxValueValidator(60)])
    hora_parto_periodo_3 = models.TimeField('Hora', blank=True, null=True)
    dirigido_parto_periodo_3 = models.CharField('Dirigido', max_length=1, choices=BOOLEAN_CHOICES, blank=True,
                                                null=True)
    sangrado_aproximado = models.SmallIntegerField('Sangrado aproximado', null=True, blank=True, validators=[
            MinValueValidator(1), MaxValueValidator(9999)])

    establecimiento = models.ForeignKey('establecimientos.Establecimiento', related_name='terminaciones_embarazo')
    paciente = models.ForeignKey('pacientes.Paciente', related_name='terminaciones_embarazo')
    ingreso = models.OneToOneField('Ingreso', related_name='terminacion_embarazo')

    terminacion = models.CharField('Terminación', max_length=20, choices=TERMINACION_CHOICES, default=PARTO_ESPONTANEO,
                                   blank=True, null=True)
    procedimiento = models.CharField('Tipo procedimiento', max_length=20, choices=PROCEDIMIENTO_CHOICES,
                                     blank=True, null=True)
    posicion_gestante = models.CharField('Posición gestante', max_length=20, choices=POSICION_CHOICES,
                                         default=POSICION_HORIZONTAL, blank=True, null=True)
    acompaniante = models.BooleanField('Parto con acompañante', default=False)
    duracion = models.CharField('Duración', max_length=20, choices=DURACION_CHOICES, default=DURACION_NORMAL,
                                blank=True, null=True)
    muerte_intrauterina = models.CharField('Muerte intrauterina', max_length=20, choices=MUERTE_INTRAUTERINA_CHOICES,
                                           default=NO_HUBO, blank=True, null=True)
    episiotomia = models.CharField('Episiotomía', max_length=1, choices=BOOLEAN_CHOICES, blank=True, null=True)
    tipo_episiotomia = models.CharField('Tipo', max_length=5, choices=TIPO_EPISIOTOMIA_CHOICES, blank=True, null=True)
    desgarro = models.CharField('Desgarro', max_length=1, choices=BOOLEAN_CHOICES, blank=True, null=True)
    desgarro_grado = models.CharField('Grado', max_length=20, choices=DESGARROS_CHOICES, blank=True, null=True)
    alumbramiento = models.CharField('Alumbramiento', max_length=20, choices=ALUMBRAMIENTO_CHOICES, blank=True,
                                     null=True)
    placenta = models.CharField('Placenta', max_length=20, default=PLACENTA_COMPLETA, null=True, blank=True,
                                choices=PLACENTA_CHOICES)
    ligadura_cordon = models.CharField('Ligadura cordón', max_length=20, choices=LIGADURA_CORDON_CHOICES, null=True,
                                       blank=True)
    cordon_umbilical = models.CharField('Cordon Umbilical', max_length=20, choices=CORDON_UMBILICAL_CHOICES, null=True,
                                        blank=True)

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='terminacion_embarazos_c')
    modifier = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='terminacion_embarazos_m')

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    referido = models.CharField('¿Es referida?', max_length=1, choices=BOOLEAN_CHOICES, default=NO)
    fecha_referido = models.DateField('Fecha Referido', blank=True, null=True)


class Placenta(models.Model):

    COMPLETA = 'C'
    INCOMPLETA = 'I'
    NONE = '-'

    DESPRENDIMIENTO_CHOICES = (
        (COMPLETA, u'Completa'),
        (INCOMPLETA, u'Incompleta')
    )

    SHULTZ = 'shultz'
    DUNCAN = 'duncan'
    TIPO_NONE = '----'
    TIPO_CHOICES = (
        (SHULTZ, 'Shultz'),
        (DUNCAN, 'Duncan')
    )

    CENTRAL = 'central'
    EXCENTRICA = 'excentrica'
    RAQUETA = 'marginal (en raqueta)'
    VELAMENTOSA = 'velamentosa'

    INSERCION_CHOICES = (
        (CENTRAL, u'Central'),
        (EXCENTRICA, u'Excentrica'),
        (RAQUETA, u'Marginal (Raqueta)'),
        (VELAMENTOSA, u'Velamentosa')
    )

    VENA_ARTERIA = '1 vena y 2 arterias'
    OTRO = 'otro'

    VASOS_CHOICES = (
        (VENA_ARTERIA, '1 vena y 2 arterias'),
        (OTRO, 'Otro')
    )

    CLARO = 'claro'
    MECONIAL = 'meconial'
    SANGUINOLENTO = 'sanguinolento'

    COLOR_CHOICES = (
        (CLARO, 'Claro'),
        (MECONIAL, 'Meconial'),
        (SANGUINOLENTO, 'Sanguinolento')
    )

    SUI = 'sui generis'
    OTRO = 'Otros'

    OLOR_CHOICES = (
        (SUI, 'Sui generis'),
        (OTRO, 'Otros')
    )

    SI = 's'
    NO = 'n'

    BOOLEAN_CHOICES = (
        (SI, 'Si'),
        (NO, 'No')
    )

    SIMPLE = 'simple'
    DOBLE = 'doble'
    TRIPLE = 'triple'

    CIRCULAR_CHOICES = (
        (SIMPLE, 'Simple'),
        (DOBLE, 'Doble'),
        (TRIPLE, 'Triple')
    )

    terminacion_embarazo = models.ForeignKey(TerminacionEmbarazo, blank=True, null=True, related_name='placentas')
    # Placenta
    placenta_desprendimiento = models.CharField('Desprendimiento', choices=DESPRENDIMIENTO_CHOICES, blank=True, null=True,
                                                max_length=1)
    placenta_tipo = models.CharField('Tipo', choices=TIPO_CHOICES, blank=True, null=True, max_length=20)
    placenta_peso = models.IntegerField('Peso', blank=True, null=True, validators=[
            MinValueValidator(0), MaxValueValidator(9999)])
    placenta_tamanio_ancho = models.IntegerField('Ancho', blank=True, null=True, validators=[
            MinValueValidator(0), MaxValueValidator(999)])
    placenta_tamanio_longitud = models.IntegerField(
        'Longitud', blank=True, null=True, validators=[
            MinValueValidator(0), MaxValueValidator(999)])
    placenta_otras_caracteristicas = models.TextField(verbose_name='Otras características', blank=True, null=True)
    # Membrana
    membranas = models.CharField('Membranas', choices=DESPRENDIMIENTO_CHOICES, blank=True, null=True,
                                 max_length=1)
    # Cordón umbilical
    cordon_umbilical_longitud = models.IntegerField('Longitud', blank=True, null=True, validators=[
            MinValueValidator(0), MaxValueValidator(999)])
    cordon_umbilical_diametro = models.IntegerField('Diametro', blank=True, null=True, validators=[
            MinValueValidator(0), MaxValueValidator(99)])
    cordon_umbilical_insercion = models.CharField('Inserción', choices=INSERCION_CHOICES, blank=True, null=True,
                                                  max_length=22)
    cordon_umbilical_vasos = models.CharField('Vasos', max_length=20, blank=True, null=True, choices=VASOS_CHOICES)
    cordon_umbilical_circular = models.CharField('Circular', max_length=1, choices=BOOLEAN_CHOICES, blank=True,
                                                 null=True)
    cordon_umbilical_circular_tipo = models.CharField('Tipo', max_length=10, choices=CIRCULAR_CHOICES, blank=True,
                                                      null=True)
    cordon_umbilical_otras_caracteristicas = models.TextField(verbose_name='Otras características', blank=True,
                                                              null=True)
    # Líquido amniótico
    liquido_amniotico_cantidad = models.IntegerField('Cantidad', null=True, blank=True, validators=[
            MinValueValidator(0), MaxValueValidator(9999)])
    liquido_amniotico_color = models.CharField('Color', choices=COLOR_CHOICES, blank=True, null=True,
                                               max_length=20)
    liquido_amniotico_olor = models.CharField('Olor', choices=OLOR_CHOICES, blank=True, null=True, max_length=20)
    liquido_amniotico_otras_caracteristicas = models.TextField(verbose_name='Otras características', blank=True,
                                                               null=True)
    otras_caracteristicas = models.TextField(verbose_name='Otras características', blank=True, null=True)
