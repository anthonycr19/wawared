# -*- coding: utf-8 -*-
# Python imports


# Django imports
from django import forms

# Third party apps imports


# Local imports
from establecimientos.models import Establecimiento, Diresa, Red, Microred


# Create your forms here.
class IndicadoresForm(forms.Form):
    INDICADORES_CHOICES = (
        ('', '-----------------------'),
        # ('1', 'Alertas de riesgo'),
        # ('2', 'Atencion de gestante complicada (por gineco obstetra)'),
        # ('3', 'Desercion de gestantes de bajo riesgo'),
        # ('4', 'Desercion de gestantes de riesgo con mensaje de alerta'),
        # ('5', 'Estratificacion de riesgo gestacional'),
        ('6', u'Gestante tamizada con prueba rapida para Sífilis'),
        ('7', 'Gestante Adolescente Atendida'),
        ('8', 'Gestante Adolescente Controlada'),
        ('9', 'Gestante Atendida'),
        ('10', 'Gestante Atendida en Psicoprofilaxis y Estimulación Prenatal'),
        ('11', 'Gestante Atendidas por trimestre'),
        # ('12', 'Gestante con 1 visita domiciliaria'),
        # ('13', 'Gestante con 2 consultas odontológicas'),
        # ('14', 'Gestante con 2 visitas domiciliarias'),
        ('16', 'Gestante con ácido fólico 1er trimestre'),
        ('17', 'Gestante con Amenaza de Aborto'),
        # ('18', 'Gestante con Amenaza de Pato Prematuro'),
        ('19', 'Gestante con Anemia'),
        ('20', u'Gestante con ecografía'),
        ('21', u'Gestante con evaluación nutricional'),
        # ('22', 'Gestante con otra omplicacion'),
        ('23', 'Gestante con PAP'),
        ('24', 'Gestante con PAP positivo'),
        ('25', 'Gestante con Pre Eclampsia'),
        # ('26', 'Gestante con resultado de Bienestar Fetal Alterado'),
        ('27', 'Gestante con resultados de análisis en 2da APN'),
        # ('28', 'Gestante con Ruptura Prematura de Membranas'),
        ('29', u'Gestante Controlada (6ta atención)'),
        # ('30', 'Gestante detectada con Depresion que recibe
        #           manejo psicológico'),
        # ('31', 'Gestante detectada con VBG que recibe manejo psicológico'),
        # ('32', 'Gestante detectada en busqueda activa'),
        ('33', 'Gestante ITU'),
        ('34', 'Gestante Preparada en Psicoprofilaxis y '
               'Estimulación Prenatal (6 sesiones)'),
        ('35', u'Gestante protegida con vacuna antitetánica (2 dosis)'),
        # ('36', 'Gestante que acude acompañada a 4 APN'),
        # ('37', 'Gestante que acude acompañada a la 1ra APN'),
        # ('38', 'Gestante que cumple con las 3 entrevistas de Plan de parto'),
        ('39', 'Gestante que inicia Plan de parto'),
        # ('40', 'Gestante que recibe taller demostrativo en
        #           nutricion saludable'),
        # ('41', 'Gestante reactiva para Proteinuria'),
        ('42', u'Gestante reactiva para Sífilis'),
        ('43', 'Gestante reactiva para VIH'),
        ('44', 'Gestante Reenfocada (paquete completo en 6ta atención)'),
        # ('45', 'Gestante tamizada con  Ac. Sulfosalicilico o
        #           tira reactiva para proteinas '),
        ('46', 'Gestante tamizada con prueba rapida para  VIH'),
        # ('47', 'Gestante tamizada con VBG'),
        # ('48', 'Malformacion fetal por ecografia'),
        # ('49', 'Morbilidad gestacional'),
        # ('50', 'N° de Casa de Espera Operativa'),
        # ('51', 'N° de casos de APP que  recibieron corticoides'),
        # ('52', 'N° de casos de Morbilidad  Materna Extrema '),
        # ('53', 'N° de casos de Muerte Materna'),
        # ('54', 'N° de casos de Muerte Perinatal'),
        # ('55', 'Nº de Abortos atendidos (AMEU+LU)'),
        # ('56', 'Produccion por Obstetra'),
    )

    diresa = forms.ModelChoiceField(
        empty_label='-----------------------',
        queryset=Diresa.objects.all(), required=False)

    red = forms.ModelChoiceField(
        empty_label='-----------------------',
        queryset=Red.objects.filter(estado=True), required=False)

    microred = forms.ModelChoiceField(
        empty_label='-----------------------',
        queryset=Microred.objects.filter(estado=True), required=False)

    establecimiento = forms.ModelChoiceField(
        empty_label='-----------------------',
        queryset=Establecimiento.objects.all(), required=False)

    indicador = forms.ChoiceField(
        choices=INDICADORES_CHOICES, label=u'Reporte Estadístico',
        required=False)
    fecha_inicio = forms.DateField(label=u'Fecha Inicio')
    fecha_final = forms.DateField(label=u'Fecha Final')

    def __init__(self, *args, **kwargs):
        super(IndicadoresForm, self).__init__(*args, **kwargs)
        self.fields['indicador'].required = True

    def clean(self):
        diresa = self.cleaned_data['diresa']
        red = self.cleaned_data['red']
        microred = self.cleaned_data['microred']
        establecimiento = self.cleaned_data['establecimiento']
        fecha_inicio = self.cleaned_data['fecha_inicio']
        fecha_final = self.cleaned_data['fecha_final']

        if diresa is None and \
                red is None and \
                microred is None and \
                establecimiento is None:
            raise forms.ValidationError(
                'Debe seleccionar algun tipo de alcance para los reportes')
        elif fecha_inicio >= fecha_final:
            self.add_error(
                'fecha_inicio',
                'La fecha de inicio debe ser menor que la fecha final.')
        else:
            return self.cleaned_data
