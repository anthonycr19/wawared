# coding: utf-8
from __future__ import unicode_literals
from datetime import datetime
from django.core.exceptions import ValidationError
from django import forms
from django.forms.models import inlineformset_factory
from controles.models import ExamenFisico
from .models import (Ingreso, Partograma, PartogramaMedicion, TerminacionEmbarazo, Placenta)


class IngresoForm(forms.ModelForm):
    class Meta:
        model = Ingreso
        exclude = ('establecimiento', 'paciente', 'embarazo')

    def __init__(self, *args, **kwargs):
        super(IngresoForm, self).__init__(*args, **kwargs)
        readonly_fields = ('eg_ecografia', 'eg_altura_uterina', 'eg_fum',
                           'fecha_probable_parto_altura_uterina',
                           'fecha_probable_parto_ecografia',
                           'fecha_probable_parto_fum')
        for field_name in readonly_fields:
            self.fields[field_name].widget.attrs['readonly'] = 'readonly'

    def clean(self):
        cd = super(IngresoForm, self).clean()
        if cd['lugar_de_derivacion'] == Ingreso.OTROS and not cd['lugar_de_derivacion_otros']:
            self.add_error('lugar_de_derivacion', ['Definir otro lugar de derivación'])
        return cd


class PartogramaMedicionForm(forms.ModelForm):
    BOOLEAN_CHOICES = (
        (True, 'Si'),
        (False, 'No'),
        (None, 'N/A')
    )

    soluciones = forms.ChoiceField(label='Soluciones', choices=BOOLEAN_CHOICES, widget=forms.RadioSelect, initial=None)

    class Meta:
        model = PartogramaMedicion
        exclude = ('partograma',)


class TerminacionEmbarazoForm(forms.ModelForm):
    hidden_name_form = forms.CharField(label='', widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(TerminacionEmbarazoForm, self).__init__(*args, **kwargs)
        self.fields['fecha'].initial = datetime.today()
        self.fields['hidden_name_form'].initial = 'terminacion'

    class Meta:
        model = TerminacionEmbarazo
        exclude = ('establecimiento', 'paciente', 'embarazo', 'ingreso', 'partograma', 'creator',
                   'modifier', 'terminacion', 'procedimiento', 'posicion_gestante', 'acompaniante',
                   'duracion', 'muerte_intrauterina', 'alumbramiento', 'placenta', 'ligadura_cordon',
                   'cordon_umbilical')


class ExamenFisicoIngresoForm(forms.ModelForm):
    BOOLEAN_CHOICES = (
        (True, u'Si'),
        (False, u'No'),
        (None, u'N/A')
    )

    piel_y_mucosas = forms.ChoiceField(choices=ExamenFisico.CN_CHOICES, widget=forms.RadioSelect)
    mamas = forms.ChoiceField(choices=ExamenFisico.CN_CHOICES, widget=forms.RadioSelect)
    respiratorio = forms.ChoiceField(choices=ExamenFisico.CN_CHOICES, widget=forms.RadioSelect)
    cardiovascular = forms.ChoiceField(choices=ExamenFisico.CN_CHOICES, widget=forms.RadioSelect)
    abdomen = forms.ChoiceField(choices=ExamenFisico.CN_CHOICES, widget=forms.RadioSelect)

    eg_dolor = forms.ChoiceField(label=u'Dolor', choices=ExamenFisico.DOLOR_CHOICES, widget=forms.RadioSelect,
                                 initial=ExamenFisico.N_A)
    eg_mal_olor = forms.ChoiceField(label=u'Mal olor', choices=BOOLEAN_CHOICES, widget=forms.RadioSelect)
    eg_fondo_de_saco = forms.ChoiceField(label=u'Fondo de saco', choices=ExamenFisico.FONDO_DE_SACO_CHOICES,
                                         widget=forms.RadioSelect)

    tv_tb_consistencia = forms.ChoiceField(label=u'Consistencia', widget=forms.RadioSelect,
                                           choices=ExamenFisico.TB_CONSISTENCIA_CHOICES, required=False)
    tv_tb_posicion = forms.ChoiceField(label=u'Posición', widget=forms.RadioSelect,
                                       choices=ExamenFisico.TB_POSICION_CHOICES, required=False)
    tv_tb_borramiento = forms.ChoiceField(label=u'Borramiento', widget=forms.RadioSelect,
                                          choices=ExamenFisico.TB_BORRAMIENTO_CHOICES, required=False)
    tv_tb_dilatacion = forms.ChoiceField(label=u'Dilatación', widget=forms.RadioSelect,
                                         choices=ExamenFisico.TB_DILATACION_CHOICES, required=False)
    tv_tb_altura_presentacion = forms.ChoiceField(label=u'Altura presentación', widget=forms.RadioSelect,
                                                  choices=ExamenFisico.TB_ALTURA_PRESENTACION_CHOICES, required=False)

    tb_fields = ('tv_tb_consistencia', 'tv_tb_posicion', 'tv_tb_borramiento',
                 'tv_tb_dilatacion', 'tv_tb_altura_presentacion', 'tv_tb_resultado')

    def clean_tv_tb_resultado(self):
        flag = True
        if self.cleaned_data['tv_tb_aplica']:
            for field in self.tb_fields:
                value = self.cleaned_data[field]
                flag = bool(value) and flag
            if not flag:
                raise forms.ValidationError(
                    'Si Test de Bishop aplica debe llenar todos '
                    'los campos de Test de Bishop')
        else:
            for field in self.tb_fields:
                self.cleaned_data[field] = None
        return self.cleaned_data['tv_tb_resultado']

    class Meta:
        model = ExamenFisico
        exclude = (
            'control', 'ingreso', 'especuloscopia', 'examen_ginecologico', 'odontologico', 'odontologico_observacion',
            'urinario', 'urinario_observacion', 'neurologico', 'neurologico_observacion', 'especuloscopia_vagina',
            'especuloscopia_fondo_de_saco', 'especuloscopia_observaciones', 'tv_cambio_cervicales', 'tv_vagina',
            'tv_utero', 'tv_hallazgos', 'tv_otros', 'tv_dilatacion', 'tv_incorporacion', 'tv_altura_presentacion',
            'tv_membranas', 'tv_membranas_rotas_tipo', 'tv_membranas_rotas_tiempo', 'tv_liquido_amniotico',
            'pelvimetria', 'pelvimetria_observacion', 'eg_posicion', 'eg_restos', 'eg_culdocentesis',
            'eg_genitales_externos')


class PlacentaForm(forms.ModelForm):
    class Meta:
        model = Placenta
        fields = (
            'placenta_desprendimiento', 'placenta_tipo', 'placenta_peso', 'placenta_tamanio_ancho',
            'placenta_tamanio_longitud', 'placenta_otras_caracteristicas', 'membranas', 'cordon_umbilical_longitud',
            'cordon_umbilical_diametro', 'cordon_umbilical_insercion', 'cordon_umbilical_vasos',
            'cordon_umbilical_circular', 'cordon_umbilical_circular_tipo', 'cordon_umbilical_otras_caracteristicas',
            'liquido_amniotico_cantidad', 'liquido_amniotico_color', 'liquido_amniotico_olor',
            'liquido_amniotico_otras_caracteristicas', 'otras_caracteristicas')


PlacentaFormSet = inlineformset_factory(TerminacionEmbarazo, Placenta, form=PlacentaForm, min_num=1, max_num=5, extra=0)
