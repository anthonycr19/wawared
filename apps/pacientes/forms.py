# -*- coding: utf-8 -*-
from datetime import date
from itertools import chain
import calendar

from django import forms

from .models import (
    Paciente, AntecedenteGinecologico, Vacuna, Etnia, HistoriaClinica,
    validate_hc_length)

from ubigeo.models import Departamento, Distrito, Provincia, Pais


class PacienteForm(forms.ModelForm):
    BOOLEAN_CHOICES = (
        (True, u'Si'),
        (False, u'No')
    )

    MONTH_CHOICES = (
        (0, u'---------'),
        (1, u'Enero'),
        (2, u'Febrero'),
        (3, u'Marzo'),
        (4, u'Abril'),
        (5, u'Mayo'),
        (6, u'Junio'),
        (7, u'Julio'),
        (8, u'Agosto'),
        (9, u'Septiembre'),
        (10, u'Octubre'),
        (11, u'Noviembre'),
        (12, u'Diciembre')
    )

    transfusion_sanguinea = forms.ChoiceField(
        widget=forms.RadioSelect, choices=BOOLEAN_CHOICES + ((None, u'N/A'),),
        initial=None)
    recibir_sms = forms.ChoiceField(
        widget=forms.RadioSelect, choices=BOOLEAN_CHOICES + ((None, u'N/A'),),
        initial=None)
    dia_nacimiento = forms.ChoiceField()
    mes_nacimiento = forms.ChoiceField(choices=MONTH_CHOICES)
    anio_nacimiento = forms.ChoiceField(initial=1987)

    hc = forms.CharField(
        label='HC', max_length=20, required=True,
        validators=[validate_hc_length])

    class Meta:
        model = Paciente
        exclude = (
            'antecedentes_familiares', 'antecedentes_medicos',
            'fecha_nacimiento', 'direccion_completa', 'historia_clinica')

    def __init__(self, *args, **kwargs):
        super(PacienteForm, self).__init__(*args, **kwargs)
        self.establecimiento_id = None
        self.fields['urbanizacion'].required = False
        self.fields['numero_documento'].required = False
        self.fields['numero_documento'].label = u'* Número documento'
        self.fields[
            'departamento_residencia'].label = '* Departamento residencia'
        self.fields['provincia_residencia'].label = '* Provincia residencia'
        self.fields['distrito_residencia'].label = '* Distrito residencia'
        self.fields['estudio'].label = '* Estudio'
        self.fields['tiempo_estudio'].label = u'* Años aprobados'
        self.fields['tiempo_estudio'].required = False
        self.fields['ocupacion'].label = u'* Ocupación'
        self.fields['estado_civil'].label = '* Estado Civil'
        self.fields['tipo_parentesco_responsable'].initial = (
            Paciente.PARENTESCO_NO_APLICA)
        self.fields['componente'].initial = Paciente.COMPONENTE_NO_APLICA
        self.fields['afiliacion'].initial = Paciente.AFILIACION_NO_APLICA

        lastday = calendar.monthrange(date.today().year, date.today().month)[1]
        dias = [('', '---')] + [(str(val), str(val)) for val in range(1, lastday)]
        self.fields['dia_nacimiento'].choices = dias

        self.fields['anio_nacimiento'].choices = (
            (val, val) for val in range(date.today().year - 5, 1950, -1))
        peru = Pais.objects.get(codigo__iexact='PE')
        self.fields['pais_residencia'].initial = peru
        self.fields['pais_residencia'].label = u'* País residencia'
        self.fields['pais_nacimiento'].initial = peru
        self.fields['pais_nacimiento'].label = u'* País nacimiento'
        self.fields['etnia'].initial = Etnia.objects.get(
            nombre__iexact='mestizo')
        self.fields['seguro_essalud'].widget.attrs = {
            'class': 'js-otro-seguro'}
        self.fields['seguro_privado'].widget.attrs = {
            'class': 'js-otro-seguro'}
        self.fields['seguro_sanidad'].widget.attrs = {
            'class': 'js-otro-seguro'}
        self.fields['seguro_otros'].widget.attrs = {'class': 'js-otro-seguro'}
        self.fields['departamento_nacimiento'].required = False
        self.fields['provincia_nacimiento'].required = False
        if self.instance.id is not None:
            self.fields['dia_nacimiento'].initial = (
                self.instance.fecha_nacimiento.day)
            self.fields['mes_nacimiento'].initial = (
                self.instance.fecha_nacimiento.month)
            self.fields['anio_nacimiento'].initial = (
                self.instance.fecha_nacimiento.year)
            if not self.data:  # when not post request
                self.fields['departamento_residencia'].queryset = (
                    Departamento.objects.filter(
                        pais=self.instance.pais_residencia))
                self.fields['provincia_residencia'].queryset = (
                    Provincia.objects.filter(
                        departamento=self.instance.departamento_residencia))
                self.fields['distrito_residencia'].queryset = (
                    Distrito.objects.filter(
                        provincia=self.instance.provincia_residencia))
                self.fields['departamento_nacimiento'].queryset = (
                    Departamento.objects.filter(
                        pais=self.instance.pais_nacimiento))
                self.fields['provincia_nacimiento'].queryset = (
                    Provincia.objects.filter(
                        departamento=self.instance.departamento_nacimiento))

    def save(self, commit=True):
        """
        Para comodidad del usuario se esta reemplazando el campo de fecha
        por tres campos correspondientes al dia, mes y año
        """
        obj = self.instance
        data = self.cleaned_data
        fecha = {
            'day': int(data['dia_nacimiento']),
            'month': int(data['mes_nacimiento']),
            'year': int(data['anio_nacimiento'])
        }
        obj.fecha_nacimiento = date(**fecha)
        return super(PacienteForm, self).save(commit)

    def clean_hc(self):
        hc = self.cleaned_data['hc']
        if not self.instance.id:  # paciente nuevo
            if HistoriaClinica.objects.filter(
                establecimiento_id=self.establecimiento_id,
                numero=hc).exists():
                raise forms.ValidationError(
                    u'El número de HC ya existe para este establecimiento')
        else:
            if HistoriaClinica.objects.filter(
                establecimiento_id=self.establecimiento_id,
                numero=hc).exclude(
                paciente__id=self.instance.id).exists():
                raise forms.ValidationError(
                    u'El número de HC ya existe para este establecimiento y'
                    'corresponde a otro paciente')
        return hc

    def clean_numero_documento(self):

        numero_documento = self.cleaned_data['numero_documento']
        tipo_documento = self.cleaned_data['tipo_documento']

        if not self.instance.id:
            try:

                if tipo_documento != 'nodoc' and tipo_documento != 'notrajo':

                    paciente = Paciente.objects.get(numero_documento=numero_documento, tipo_documento=tipo_documento)

                    if not paciente is None:
                        raise forms.ValidationError(u'Numero de documento existente, ''paciente ya registrada')

                else:
                    numero_documento = "#temp#"
            except Paciente.DoesNotExist:
                if tipo_documento != 'nodoc' and numero_documento == '':
                    raise forms.ValidationError('Este campo es obligatorio.')
        else:
            if (tipo_documento != 'nodoc' or tipo_documento != 'notrajo') and numero_documento == '':
                raise forms.ValidationError('Este campo es obligatorio.')
        return numero_documento

    def set_establecimiento_id(self, establecimiento_id):

        self.establecimiento_id = establecimiento_id

    def set_hc_value(self):

        self.fields['hc'].initial = HistoriaClinica.objects.get(
            establecimiento_id=self.establecimiento_id,
            paciente_id=self.instance.id).numero

    def clean_tiempo_estudio(self):

        tiempo_estudio = self.cleaned_data['tiempo_estudio']
        try:
            estudio = self.cleaned_data['estudio']
            if estudio.nombre != 'Analfabeta' and tiempo_estudio is None:
                self.add_error(
                    'tiempo_estudio',
                    'Este campo es obligatorio.')
            else:
                return tiempo_estudio
        except Exception as e:
            print
            str(e)

class AntecedenteGinecologicoForm(forms.ModelForm):
    def clean_edad_menarquia(self):
        primera_menarquia = self.cleaned_data['edad_menarquia']
        if primera_menarquia <= self.instance.paciente.edad:
            return primera_menarquia
        else:
            raise forms.ValidationError(
                u'Edad de menarquia sexual debe ser menor a la edad de la'
                'paciente')

    def clean_edad_primera_relacion_sexual(self):
        primera_relacion_sexual = (
            self.cleaned_data['edad_primera_relacion_sexual'])
        if self.cleaned_data['edad_menarquia'] <= primera_relacion_sexual \
            <= self.instance.paciente.edad:
            return primera_relacion_sexual
        else:
            if self.cleaned_data['edad_menarquia'] > primera_relacion_sexual:
                raise forms.ValidationError(
                    u'Edad de primera relación sexual debe ser mayor o igual'
                    'a la edad de menarquia')
            if primera_relacion_sexual >= self.instance.paciente.edad:
                raise forms.ValidationError(
                    u'Edad de primera relación sexual debe ser menor a la edad'
                    'de la paciente')

    class Meta:
        model = AntecedenteGinecologico
        exclude = ('paciente',)


class VacunaForm(forms.ModelForm):
    BOOLEAN_CHOICES = (
        (True, u'Si'),
        (False, u'No'),
        (None, u'N/A')
    )

    antitetanica_primera_dosis = forms.ChoiceField(
        label=u'Primera dosis', choices=BOOLEAN_CHOICES,
        widget=forms.RadioSelect)
    antitetanica_segunda_dosis = forms.ChoiceField(
        label=u'Segunda dosis', choices=BOOLEAN_CHOICES,
        widget=forms.RadioSelect)
    antitetanica_tercera_dosis = forms.ChoiceField(
        label=u'Tercera dosis', choices=BOOLEAN_CHOICES,
        widget=forms.RadioSelect)

    class Meta:
        model = Vacuna
        exclude = ('paciente',)

class VacunaPreForm(forms.ModelForm):

    class Meta:
        model = Vacuna
        exclude = ('paciente','antitetanica_numero_dosis_previas','antitetanica_primera_dosis',
        'antitetanica_primera_dosis_valor', 'antitetanica_segunda_dosis', 'antitetanica_segunda_dosis_valor',
        'antitetanica_tercera_dosis', 'antitetanica_tercera_dosis_valor')


class HistoriaClinicaForm(forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        exclude = ('establecimiento', 'paciente')
