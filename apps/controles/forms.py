# coding:utf-8
from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from ubigeo.models import Departamento, Provincia
from establecimientos.models import Establecimiento
from partos.models import PartogramaMedicion,Ingreso

from .models import Control, ExamenFisico, Laboratorio, Diagnostico, ExamenFisicoFetal


class ControlForm(forms.ModelForm):
    class Meta:
        model = Control
        exclude = (
            'establecimiento', 'embarazo', 'paciente', 'visito_sintomas',
            'visito_diagnostico', 'atencion_hora')
        labels = {
            'fcf': u'',
            'situacion': u'',
            'presentacion': u'',
            'posicion': u'',
            'movimientos_fetales': u'',
            'imc': u'IMC'
        }

    def __init__(self, *args, **kwargs):

        establecimiento_id = kwargs.pop('establecimiento_id')
        establecimiento_actual = Establecimiento.objects.get(id=establecimiento_id)
        super(ControlForm, self).__init__(*args, **kwargs)

        if establecimiento_actual.is_sistema_externo_admision:
            self.fields['proxima_cita'].widget = forms.HiddenInput()
            self.fields['proxima_cita'].required = False

        self.fields['eg_fum'].widget.attrs['readonly'] = 'True'
        self.fields['eg_ecografia'].widget.attrs['readonly'] = 'True'
        self.fields['eg_altura_uterina'].widget.attrs['readonly'] = 'True'
        self.fields['fecha_probable_parto_fum'].widget.attrs[
            'readonly'] = 'True'
        self.fields['fecha_probable_parto_ecografia'].widget.attrs[
            'readonly'] = 'True'
        self.fields['fecha_probable_parto_altura_uterina'].widget.attrs[
            'readonly'] = 'True'
        self.fields['temperatura'].widget.attrs = {'step': 0.1}
        self.fields['altura_uterina'].required = False
        self.fields['fcf'].required = False
        self.fields['presion_sistolica'].required = True
        self.fields['presion_diastolica'].required = True

        if not self.data:
            self.fields['zika_departamento'].queryset = (
                Departamento.objects.filter(pais=self.instance.zika_pais))
            self.fields['zika_provincia'].queryset = (
                Provincia.objects.filter(
                    departamento=self.instance.zika_departamento))

    def clean_atencion_fecha(self):
        fecha = self.cleaned_data.get('atencion_fecha', '')
        if fecha and isinstance(fecha, datetime) and \
            self.instance.embarazo.controles.filter(
                atencion_fecha=fecha).exists():
            raise ValidationError(
                'Ya existe registrado un control para esta fecha')
        return fecha

    def clean_proxima_cita(self):
        cita = self.cleaned_data['proxima_cita']
        if cita:

            atencion = self.cleaned_data.get('atencion_fecha')

            if not atencion:
                raise forms.ValidationError(
                    u'La fecha de atención no puede se vacío.'
                )

            if cita <= atencion:
                raise forms.ValidationError(
                    u'La fecha de la cita no puede ser menor o igual '
                    u'a la fecha de atención')

        return cita

    def clean_altura_uterina(self):
        altura_uterina = self.cleaned_data['altura_uterina']

        '''
        if self.cleaned_data['eg_elegida'] == 'fum' and \
                self.cleaned_data['eg_fum'].__len__() > 0:
            edad_gestacional_semanas = int(
                self.cleaned_data['eg_fum'].split()[0])
        elif self.cleaned_data['eg_elegida'] == 'ecografia' and \
                self.cleaned_data['eg_ecografia'].__len__() > 0:
            edad_gestacional_semanas = int(
                self.cleaned_data['eg_ecografia'].split()[0])
        elif self.cleaned_data['eg_elegida'] == 'altura uterina' and \
                self.cleaned_data['eg_altura_uterina'].__len__() > 0:
            edad_gestacional_semanas = int(
                self.cleaned_data['eg_altura_uterina'].split()[0])
        else:
            edad_gestacional_semanas = None

        if edad_gestacional_semanas is not None:
            if edad_gestacional_semanas >= 12:
                if altura_uterina <= 0 or altura_uterina > 100:
                    raise forms.ValidationError(
                        u'La altura uterina debe ser un número positivo '
                        'de maximo 2 cifras')
        '''
        if altura_uterina:
            if altura_uterina <= 0 or altura_uterina >= 100:
                raise forms.ValidationError(
                    u'La altura uterina debe ser un número positivo '
                    'de maximo 2 cifras')

        return altura_uterina

    '''def clean_fcf(self):
        fcf = self.cleaned_data['fcf']

        if self.cleaned_data['eg_elegida'] == 'fum' and \
                self.cleaned_data['eg_fum'].__len__() > 0:
            edad_gestacional_semanas = int(
                self.cleaned_data['eg_fum'].split()[0])
        elif self.cleaned_data['eg_elegida'] == 'ecografia' and \
                self.cleaned_data['eg_ecografia'].__len__() > 0:
            edad_gestacional_semanas = int(
                self.cleaned_data['eg_ecografia'].split()[0])
        elif self.cleaned_data['eg_elegida'] == 'altura uterina' and \
                self.cleaned_data['eg_altura_uterina'].__len__() > 0:
            edad_gestacional_semanas = int(
                self.cleaned_data['eg_altura_uterina'].split()[0])
        else:
            edad_gestacional_semanas = None

        if edad_gestacional_semanas is not None:
            if edad_gestacional_semanas > 19:
                if fcf < 120 or fcf > 400:
                    raise forms.ValidationError(
                        u'Asegúrese de que este valor esta entre 120 y 400')

        return fcf'''

    def set_embarazo(self, embarazo):
        self.instance.embarazo = embarazo


class ExamenFisicoFetalForm(forms.ModelForm):
    control = None
    eliminado = eliminado = forms.CharField(widget=forms.HiddenInput(),
                                            required=False)  # forms.BooleanField(initial=False, required= False)

    class Meta:
        model = ExamenFisicoFetal

        labels = {
            'fcf': u'',
            'situacion': u'',
            'presentacion': u'',
            'posicion': u'',
            'movimientos_fetales': u'',
            'visible': u'',
        }

    def __init__(self, *args, **kwargs):
        super(ExamenFisicoFetalForm, self).__init__(*args, **kwargs)

    def get_eliminado(self):
        return self['eliminado'].value()

    def set_control(self, control):

        self.control = control

    def clean_fcf(self):

        fcf = self.cleaned_data['fcf']

        if self.get_eliminado():
            return fcf

        if self.control:
            control = self.control
        else:
            control = self.instance.control

        eg_elegida = control.eg_elegida

        if eg_elegida == 'fum' and \
                control.eg_fum.__len__() > 0:
            edad_gestacional_semanas = int(
                control.eg_fum.split()[0])
        elif eg_elegida == 'ecografia' and \
                control.eg_ecografia.__len__() > 0:
            edad_gestacional_semanas = int(
                control.eg_ecografia.split()[0])
        elif eg_elegida == 'altura uterina' and \
                control.eg_altura_uterina.__len__() > 0:
            edad_gestacional_semanas = int(
                control.eg_altura_uterina.split()[0])
        else:
            edad_gestacional_semanas = None

        if edad_gestacional_semanas is not None:
            if edad_gestacional_semanas > 19:
                if fcf < 120 or fcf > 400:
                    raise forms.ValidationError(u'Asegúrese de que este valor esta entre 120 y 400')
        # self.add_error('fcf','Asegúrese de que este valor esta entre 120 y 400')

        return fcf


ExamenFisicoFetalFormSet = inlineformset_factory(Control, ExamenFisicoFetal, form=ExamenFisicoFetalForm, min_num=1,
                                                 max_num=5, extra=0)


class ExamenFisicoForm(forms.ModelForm):
    BOOLEAN_CHOICES = (
        (True, u'Si'),
        (False, u'No'),
        (None, u'N/A')
    )

    piel_y_mucosas = forms.ChoiceField(
        choices=ExamenFisico.CN_CHOICES, widget=forms.RadioSelect)
    mamas = forms.ChoiceField(
        choices=ExamenFisico.CN_CHOICES, widget=forms.RadioSelect)
    respiratorio = forms.ChoiceField(
        choices=ExamenFisico.CN_CHOICES, widget=forms.RadioSelect)
    cardiovascular = forms.ChoiceField(
        choices=ExamenFisico.CN_CHOICES, widget=forms.RadioSelect)
    odontologico = forms.ChoiceField(
        choices=ExamenFisico.CN_CHOICES, widget=forms.RadioSelect)
    abdomen = forms.ChoiceField(
        choices=ExamenFisico.CN_CHOICES, widget=forms.RadioSelect)
    urinario = forms.ChoiceField(
        choices=ExamenFisico.CN_CHOICES, widget=forms.RadioSelect)
    neurologico = forms.ChoiceField(
        choices=ExamenFisico.CN_CHOICES, widget=forms.RadioSelect)
    pelvimetria = forms.ChoiceField(
        choices=ExamenFisico.PELVIMETRIA_CHOICES, widget=forms.RadioSelect)
    examen_ginecologico = forms.ChoiceField(
        label=u'Examen Gineco-Obstétrico', choices=BOOLEAN_CHOICES,
        widget=forms.RadioSelect, initial=None)
    especuloscopia = forms.ChoiceField(
        label=u'Especuloscopia', choices=BOOLEAN_CHOICES,
        widget=forms.RadioSelect, initial=None)
    tv_cambio_cervicales = forms.ChoiceField(
        label=u'Cambios cervicales', choices=BOOLEAN_CHOICES,
        widget=forms.RadioSelect, initial=None)

    tv_tb_consistencia = forms.ChoiceField(
        label=u'Consistencia', widget=forms.RadioSelect,
        choices=ExamenFisico.TB_CONSISTENCIA_CHOICES, required=False)
    tv_tb_posicion = forms.ChoiceField(
        label=u'Posición', widget=forms.RadioSelect,
        choices=ExamenFisico.TB_POSICION_CHOICES, required=False)
    tv_tb_borramiento = forms.ChoiceField(
        label=u'Borramiento', widget=forms.RadioSelect,
        choices=ExamenFisico.TB_BORRAMIENTO_CHOICES, required=False)
    tv_tb_dilatacion = forms.ChoiceField(
        label=u'Dilatación', widget=forms.RadioSelect,
        choices=ExamenFisico.TB_DILATACION_CHOICES, required=False)
    tv_tb_altura_presentacion = forms.ChoiceField(
        label=u'Altura presentación', widget=forms.RadioSelect,
        choices=ExamenFisico.TB_ALTURA_PRESENTACION_CHOICES, required=False)

    eg_dolor = forms.ChoiceField(
        label=u'Dolor', choices=ExamenFisico.DOLOR_CHOICES,
        widget=forms.RadioSelect, initial=ExamenFisico.N_A)
    eg_posicion = forms.ChoiceField(
        label=u'Posición', choices=ExamenFisico.POSICION_CHOICES,
        widget=forms.RadioSelect)
    eg_restos = forms.ChoiceField(
        label=u'Restos', choices=ExamenFisico.RESTOS_CHOICES,
        widget=forms.RadioSelect)
    eg_culdocentesis = forms.ChoiceField(
        label=u'Culdocentesis', choices=BOOLEAN_CHOICES,
        widget=forms.RadioSelect)
    eg_fondo_de_saco = forms.ChoiceField(
        label=u'Fondo de saco', choices=ExamenFisico.FONDO_DE_SACO_CHOICES,
        widget=forms.RadioSelect)
    eg_mal_olor = forms.ChoiceField(
        label=u'Mal olor', choices=BOOLEAN_CHOICES, widget=forms.RadioSelect)

    tb_fields = (
        'tv_tb_consistencia', 'tv_tb_posicion', 'tv_tb_borramiento',
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
        exclude = ('control',)
        labels = {
            'tv_altura_presentacion': u'Descenso cefálico'
        }


class LaboratorioForm(forms.ModelForm):
    grupo = forms.ChoiceField(
        label=u'Grupo', choices=Laboratorio.GRUPO_CHOICES,
        widget=forms.RadioSelect, required=False)
    factor = forms.ChoiceField(
        label=u'Factor RH', choices=Laboratorio.FACTOR_CHOICES,
        widget=forms.RadioSelect, required=False)

    glicemia_1 = forms.ChoiceField(
        label=u'Glicemia 1', choices=Laboratorio.NORMAL_ANORMAL_NO_SE_HIZO,
        widget=forms.RadioSelect)
    glicemia_2 = forms.ChoiceField(
        label=u'Glicemia 2', choices=Laboratorio.NORMAL_ANORMAL_NO_SE_HIZO,
        widget=forms.RadioSelect)
    tolerancia_glucosa = forms.ChoiceField(
        label=u'Tolerancia glucosa',
        choices=Laboratorio.NORMAL_ANORMAL_CHOICES, widget=forms.RadioSelect)

    rapida_proteinuria = forms.ChoiceField(
        label=u'Prueba rápida de Proteinuria',
        choices=Laboratorio.REACTIVO_NO_REACTIVO_CHOICES,
        widget=forms.RadioSelect, initial=Laboratorio.NO_SE_HIZO)
    rapida_proteinuria_2 = forms.ChoiceField(
        label=u'Prueba rápida de Proteinuria',
        choices=Laboratorio.REACTIVO_NO_REACTIVO_CHOICES,
        widget=forms.RadioSelect, initial=Laboratorio.NO_SE_HIZO)
    rapida_proteinuria_3 = forms.ChoiceField(
        label=u'Prueba rápida de Proteinuria',
        choices=Laboratorio.REACTIVO_NO_REACTIVO_CHOICES,
        widget=forms.RadioSelect, initial=Laboratorio.NO_SE_HIZO)

    vdrl_rp_1 = forms.ChoiceField(
        label=u'VDRL/RPR 1',
        choices=Laboratorio.REACTIVO_NO_REACTIVO_NO_SE_HIZO,
        widget=forms.RadioSelect)
    vdrl_rp_2 = forms.ChoiceField(
        label=u'VDRL/RPR 2', choices=Laboratorio.REACTIVO_NO_REACTIVO_CHOICES,
        widget=forms.RadioSelect)
    fta_abs = forms.ChoiceField(
        label=u'FTA Abs', choices=Laboratorio.REACTIVO_NO_REACTIVO_CHOICES,
        widget=forms.RadioSelect)
    tpha = forms.ChoiceField(
        label=u'THPA', choices=Laboratorio.REACTIVO_NO_REACTIVO_CHOICES,
        widget=forms.RadioSelect)
    rapida_sifilis = forms.ChoiceField(
        label=u'Primera prueba rápida sífilis',
        choices=Laboratorio.REACTIVO_NO_REACTIVO_NO_SE_HIZO,
        widget=forms.RadioSelect)
    rapida_sifilis_2 = forms.ChoiceField(
        label=u'Segunda prueba rápida sífilis',
        choices=Laboratorio.REACTIVO_NO_REACTIVO_CHOICES,
        widget=forms.RadioSelect)
    rapida_vih_1 = forms.ChoiceField(
        label=u'Primera prueba rápida VIH',
        choices=Laboratorio.REACTIVO_NO_REACTIVO_NO_SE_HIZO,
        widget=forms.RadioSelect)
    rapida_vih_2 = forms.ChoiceField(
        label=u'Segunda prueba rápida VIH',
        choices=Laboratorio.REACTIVO_NO_REACTIVO_CHOICES,
        widget=forms.RadioSelect)
    elisa = forms.ChoiceField(
        label=u'ELISA VIH', choices=Laboratorio.REACTIVO_NO_REACTIVO_CHOICES,
        widget=forms.RadioSelect)

    ifi_western_blot = forms.ChoiceField(
        label=u'IFI/Western Blot',
        choices=Laboratorio.POSITIVO_NEGATIVO_CHOICES,
        widget=forms.RadioSelect)
    htlv_1 = forms.ChoiceField(
        label=u'HTLV 1', choices=Laboratorio.POSITIVO_NEGATIVO_CHOICES,
        widget=forms.RadioSelect)
    torch = forms.ChoiceField(
        label=u'TORCH', choices=Laboratorio.POSITIVO_NEGATIVO_CHOICES,
        widget=forms.RadioSelect)
    pcr_zika = forms.ChoiceField(
        label=u'PCR Zika', choices=Laboratorio.POSITIVO_NEGATIVO_CHOICES,
        widget=forms.RadioSelect)
    gota_gruesa = forms.ChoiceField(
        label=u'Gota gruesa', choices=Laboratorio.POSITIVO_NEGATIVO_CHOICES,
        widget=forms.RadioSelect)
    malaria_prueba_rapida = forms.ChoiceField(
        label=u'Malaria prueba rápida',
        choices=Laboratorio.POSITIVO_NEGATIVO_CHOICES,
        widget=forms.RadioSelect)
    fluorencia_malaria = forms.ChoiceField(
        label=u'Fluorescencia malaria',
        choices=Laboratorio.POSITIVO_NEGATIVO_CHOICES,
        widget=forms.RadioSelect)
    examen_completo_orina_1 = forms.ChoiceField(
        label=u'Examen completo orina 1',
        choices=Laboratorio.POSITIVO_NEGATIVO_NO_SE_HIZO,
        widget=forms.RadioSelect)
    examen_completo_orina_2 = forms.ChoiceField(
        label=u'Examen completo orina 2',
        choices=Laboratorio.POSITIVO_NEGATIVO_NO_SE_HIZO,
        widget=forms.RadioSelect)

    leucocituria = forms.ChoiceField(
        label=u'Leucocituria',
        choices=Laboratorio.POSITIVO_NEGATIVO_NO_SE_HIZO,
        widget=forms.RadioSelect)
    nitritos = forms.ChoiceField(
        label=u'Nitritos', choices=Laboratorio.POSITIVO_NEGATIVO_NO_SE_HIZO,
        widget=forms.RadioSelect)
    urocultivo = forms.ChoiceField(
        label=u'Urocultivo', choices=Laboratorio.POSITIVO_NEGATIVO_CHOICES,
        widget=forms.RadioSelect)
    bk_en_esputo = forms.ChoiceField(
        label=u'BK en esputo', choices=Laboratorio.POSITIVO_NEGATIVO_CHOICES,
        widget=forms.RadioSelect)
    listeria = forms.ChoiceField(
        label=u'Listeria', choices=Laboratorio.POSITIVO_NEGATIVO_CHOICES,
        widget=forms.RadioSelect)
    tamizaje_hepatitis_b = forms.ChoiceField(
        label=u'Tamizaje hepatitis B',
        choices=Laboratorio.POSITIVO_NEGATIVO_CHOICES,
        widget=forms.RadioSelect)

    pap = forms.ChoiceField(
        label=u'PAP', choices=Laboratorio.NORMAL_ANORMAL_NO_SE_HIZO,
        widget=forms.RadioSelect)
    iva = forms.ChoiceField(
        label=u'IVA', choices=Laboratorio.NORMAL_ANORMAL_CHOICES,
        widget=forms.RadioSelect)
    colposcopia = forms.ChoiceField(
        label=u'Colposcopia', choices=Laboratorio.NORMAL_ANORMAL_CHOICES,
        widget=forms.RadioSelect)

    class Meta:
        model = Laboratorio
        exclude = ('control', 'embarazo', 'paciente')

    def __init__(self, *args, **kwargs):
        super(LaboratorioForm, self).__init__(*args, **kwargs)

        atributos = {'class': 'hemoglobina', 'step': 0.01}

        self.fields['rapida_hemoglobina_resultado'].widget.attrs = atributos
        self.fields['hemoglobina_1_resultado'].widget.attrs = atributos
        self.fields['hemoglobina_2_resultado'].widget.attrs = atributos
        self.fields['hemoglobina_3_resultado'].widget.attrs = atributos
        self.fields['hemoglobina_4_resultado'].widget.attrs = atributos
        self.fields['hemoglobina_5_resultado'].widget.attrs = atributos
        self.fields['hemoglobina_alta_resultado'].widget.attrs = atributos

        for key in self.fields:
            field = self.fields[key]
            if field.label.lower() == 'fecha':
                field.widget.attrs['class'] = 'input-datepicker'

    def clean_rapida_sifilis_fecha(self):
        sifilis = self.cleaned_data['rapida_sifilis']
        fecha = self.cleaned_data['rapida_sifilis_fecha']

        '''if sifilis=='reactivo' or sifilis=='no reactivo':
            if fecha:
                return fecha
            else:
                raise forms.ValidationError(
                    u'Ingrese la fecha')

        return fecha'''
        return self.validacion_fecha(sifilis, fecha)

    def clean_rapida_sifilis_2_fecha(self):
        sifilis = self.cleaned_data['rapida_sifilis_2']
        fecha = self.cleaned_data['rapida_sifilis_2_fecha']

        return self.validacion_fecha(sifilis, fecha)

    def clean_rapida_vih_1_fecha(self):
        vih = self.cleaned_data['rapida_vih_1']
        fecha = self.cleaned_data['rapida_vih_1_fecha']

        return self.validacion_fecha(vih, fecha)

    def clean_rapida_vih_2_fecha(self):
        vih = self.cleaned_data['rapida_vih_2']
        fecha = self.cleaned_data['rapida_vih_2_fecha']

        return self.validacion_fecha(vih, fecha)

    def validacion_fecha(self, campo, fecha):

        if campo == 'reactivo' or campo == 'no reactivo':
            if fecha:
                return fecha
            else:
                raise forms.ValidationError(
                    u'Ingrese la fecha')

        return fecha


class DiagnosticoForm(forms.ModelForm):
    eg_elegida = forms.ChoiceField(
        label=u'Edad gestacional elegida', choices=Control.EG_CHOICES)

    class Meta:
        model = Diagnostico
        exclude = ('paciente', 'control')

    def __init__(self, *args, **kwargs):

        establecimiento_id = kwargs.pop('establecimiento_id')
        establecimiento_actual = Establecimiento.objects.get(id=establecimiento_id)
        super(DiagnosticoForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            self.fields[
                'eg_elegida'].initial = self.instance.control.eg_elegida

        if establecimiento_actual.is_sistema_externo_admision:
            self.fields['proxima_cita'].widget = forms.HiddenInput()
            self.fields['proxima_cita'].required = False

class ExamenFetalForm(forms.ModelForm):
    class Meta:
        model = ExamenFisicoFetal
        exclude = ('control','situacion','presentacion', 'posicion', 'movimientos_fetales')

ExamenFetalFormSet = inlineformset_factory(
                        Ingreso,
                        ExamenFisicoFetal,
                        form=ExamenFetalForm,
                        min_num=1,
                        max_num=12,
                        extra=0
                        )

ExamenFetalMedicionFormSet = inlineformset_factory(
                                PartogramaMedicion,
                                ExamenFisicoFetal,
                                form=ExamenFetalForm,
                                min_num=1,
                                max_num=12,
                                extra=0
                                )
