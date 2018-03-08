# coding:utf-8
from datetime import date

from django import forms
from django.forms.models import inlineformset_factory

from .models import (
    Bebe, Ecografia, EcografiaDetalle, Embarazo, FichaProblema, FichaViolenciaFamiliar, PlanParto,
    UltimoEmbarazo, ZERO_TO_3_CHOICES)


class UltimoEmbarazoForm(forms.ModelForm):
    class Meta:
        model = UltimoEmbarazo
        exclude = ('paciente', 'establecimiento', 'numero', 'embarazo')


class BebeForm(forms.ModelForm):
    BOOLEAN_CHOICES = (
        (True, u'Si'),
        (False, u'No')
    )

    MONTH_CHOICES = (
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

    vive = forms.ChoiceField(
        label=u'Vive', choices=BOOLEAN_CHOICES, initial=True)
    day = forms.ChoiceField()
    month = forms.ChoiceField(choices=MONTH_CHOICES)
    year = forms.ChoiceField()

    peso = forms.FloatField(min_value=100, max_value=9999)
    edad_gestacional = forms.IntegerField(min_value=0)

    def __init__(self, *args, **kwargs):
        """
        Se añade el key como clase para hacer las validaciones en el frontend
        """
        super(BebeForm, self).__init__(*args, **kwargs)
        self.fields['day'].choices = ((val, val) for val in range(1, 32))
        self.fields['peso'].required = False
        self.fields['year'].choices = ((val, val) for val in range(date.today().year, 1950, -1))
        self.fields['observacion'].widget.attrs['rows'] = 3
        for key in self.fields:
            field = self.fields[key]
            if key not in ('year', 'day', 'month'):
                field.widget.attrs['class'] = key + ' form-control input-sm'
            else:
                field.widget.attrs['class'] = key + ' input-sm select-gray-border'
        if self.instance.id:
            if not self.instance.no_recuerda_fecha:
                self.fields['day'].initial = self.instance.fecha.day
                self.fields['month'].initial = self.instance.fecha.month
                self.fields['year'].initial = self.instance.fecha.year

    def save(self, commit=True):
        """
        Para comodidad del usuario se esta reemplazando el campo de fecha
        por tres campos correspondientes al dia, mes y año
        """
        obj = self.instance
        data = self.cleaned_data
        fecha = {
            'day': int(data['day']),
            'month': int(data['month']),
            'year': int(data['year'])
        }

        if obj.no_recuerda_fecha:
            obj.fecha = None
        else:
            obj.fecha = date(**fecha)

        return super(BebeForm, self).save(commit)

    def clean_peso(self):
        peso = self.cleaned_data['peso']
        terminacion = self.cleaned_data['terminacion']

        if peso in xrange(0, 9501):
            return peso
        else:
            if terminacion == Bebe.TERMINACION_ABORTO or \
                    terminacion == Bebe.TERMINACION_ABORTO_MOLAR or \
                    terminacion == Bebe.TERMINACION_OBITO or \
                    terminacion == Bebe.TERMINACION_ECTOPICO:
                return peso
            else:
                raise forms.ValidationError(
                    u'Peso debe ser mayor o igual a 100')

    def clean_edad_gestacional(self):
        edad_gestacional = self.cleaned_data['edad_gestacional']
        terminacion = self.cleaned_data['terminacion']
        if terminacion == Bebe.TERMINACION_ABORTO:
            if edad_gestacional <= 20:
                return edad_gestacional
            else:
                raise forms.ValidationError(
                    u'Para terminación aborto la EG no puede ser mayor a '
                    '20 semanas')
        elif terminacion == Bebe.TERMINACION_OBITO:
            if edad_gestacional >= 20:
                return edad_gestacional
            else:
                raise forms.ValidationError(
                    u'Para terminación obito la EG no puede ser menor a '
                    '20 semanas')
        if edad_gestacional in xrange(1, 45):
            return edad_gestacional
        else:
            raise forms.ValidationError(
                u'Edad gestacional debe estar en el rango de 1 a 44')

    class Meta:
        model = Bebe
        exclude = ('fecha',)


BebeCreateFormset = inlineformset_factory(
    UltimoEmbarazo, Bebe, form=BebeForm, can_delete=True, extra=1)
BebeUpdateFormset = inlineformset_factory(
    UltimoEmbarazo, Bebe, form=BebeForm, can_delete=True, extra=0)


class EmbarazoForm(forms.ModelForm):
    def clean_talla(self):
        talla = self.cleaned_data['talla']
        if 100 <= talla <= 250:
            return talla
        else:
            raise forms.ValidationError(
                u'La talla debe estar entre los valores 100 y 250')

    perdida_interes_placer = forms.ChoiceField(
        label=u'Poco interés o placer en hacer las cosas',
        widget=forms.RadioSelect, choices=ZERO_TO_3_CHOICES, required=False)
    triste_deprimida_sin_esperanza = forms.ChoiceField(
        label=u'Sentirse desanimado/a, deprimido/a, triste o sin esperanza',
        widget=forms.RadioSelect, choices=ZERO_TO_3_CHOICES, required=False)

    class Meta:
        model = Embarazo
        exclude = (
            'paciente', 'establecimiento', 'activo',
            'hospitalizacion_diagnosticos', 'emergencia_diagnosticos', 'numero_cigarros_diarios')
        widgets = {
            'depresion_puntaje': forms.HiddenInput()
        }
        labels = {
            'imc': u'IMC pregestacional'
        }

    def __init__(self, *args, **kwargs):
        super(EmbarazoForm, self).__init__(*args, **kwargs)
        self.fields['imc'].widget.attrs['readonly'] = 'True'
        self.fields['fum'].required = False
        self.fields[
            'fecha_probable_parto_ultima_menstruacion'].widget.attrs[
            'readonly'] = 'True'


class FichaViolenciaFamiliarForm(forms.ModelForm):
    BOOLEAN_CHOICES = (
        (True, u'Si'),
        (False, u'No'),
        (None, u'N/A')
    )

    agresores = forms.CharField(
        label=u'¿Quién?', widget=forms.Textarea, required=False)

    class Meta:
        model = FichaViolenciaFamiliar
        exclude = ('paciente', 'embarazo')
        labels = {
            'violencia_psicologica': u'¿Se ha sentido alguna vez maltratado(a)'
                                     u' psicológicamente por un miembro de su familia o ajena a esta?',
            'violencia_fisica': u'¿A sido agredido(a) físicamente por un '
                                u'miembro de su familia o ajena a esta?',
            'violencia_sexual': u'¿Se ha sentido o a sido forzado(a) '
                                u'alguna vez a tener relaciones sexuales?',
            'violencia_fisica_agresores': u' ¿Quien?',
            'violencia_psicologica_agresores': u' ¿Quien?',
            'violencia_sexual_agresores': u' ¿Quien?'
        }

    def __init__(self, *args, **kwargs):
        super(FichaViolenciaFamiliarForm, self).__init__(*args, **kwargs)


class FichaProblemaForm(forms.ModelForm):
    poco_interes_o_placer = forms.ChoiceField(
        label=u'Poco interés o placer en hacer las cosas',
        choices=FichaProblema.COMMON_CHOICES, widget=forms.RadioSelect,
        required=False)
    desanimada_deprimida = forms.ChoiceField(
        label=u'Sentirse desanimado/a, deprimido/a, triste o sin esperanza',
        choices=FichaProblema.COMMON_CHOICES, widget=forms.RadioSelect,
        required=False)
    problemas_dormir = forms.ChoiceField(
        label=u'Problemas para dormir o en mantenerse dormido/a, '
              'o en dormir demasiado', choices=FichaProblema.COMMON_CHOICES,
        widget=forms.RadioSelect, required=False)
    cansancio = forms.ChoiceField(
        label=u'Sentirse cansado/a o tener poca energía',
        choices=FichaProblema.COMMON_CHOICES, widget=forms.RadioSelect,
        required=False)
    alimenticio = forms.ChoiceField(
        label=u'Tener poco apetito o comer en exceso',
        choices=FichaProblema.COMMON_CHOICES, widget=forms.RadioSelect,
        required=False)
    falta_autoestima = forms.ChoiceField(
        label=u'Sentirse mal acerca de sí mismo/a -- o sentir que es un/a '
              u'fracasado/a o que se ha fallado a sí mismo/a o asu familia',
        choices=FichaProblema.COMMON_CHOICES, widget=forms.RadioSelect,
        required=False)
    dificultad_concentracion = forms.ChoiceField(
        label=u'Dificultad para poner atención, concetrarse en cosas tales '
              u'como leer el periódico o ver televisión',
        choices=FichaProblema.COMMON_CHOICES, widget=forms.RadioSelect,
        required=False)
    mueve_lento_o_hiperactivo = forms.ChoiceField(
        label=u'Moverse o hablar tan despacio que otra personas lo pueden '
              'haber notado o lo contrario: estar tan inquieto/a o intranquilo/a '
              'que se ha estado moviendo mucho mas de lo normal',
        choices=FichaProblema.COMMON_CHOICES, widget=forms.RadioSelect,
        required=False)
    pensamientos_autodestructivos = forms.ChoiceField(
        label=u'Pensamientos de que sería mejor estar muerto/a o quisiera '
              u'hacerse daño de alguna forma', choices=FichaProblema.COMMON_CHOICES,
        widget=forms.RadioSelect, required=False)
    difucultad_cumplir_labores = forms.ChoiceField(
        label=u'Si marco algún problema, ¿Cuánto le han dificultado estos '
              'problemas realizar su trabajo, encargarse de las cosas en la casa, '
              'o llevarse bien con otras personas',
        choices=FichaProblema.CUMPLIR_LABORES_CHOICES,
        widget=forms.RadioSelect, required=False)

    class Meta:
        model = FichaProblema
        exclude = ('paciente', 'embarazo')
        widgets = {
            'puntaje': forms.HiddenInput()
        }


class EcografiaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EcografiaForm, self).__init__(*args, **kwargs)
        self.fields['biometria_fetal'].required = False
        self.fields['ila'].required = False
        self.fields['fecha'].required = False

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']

        if fecha:
            today = date.today()
            diff = today - fecha
            if fecha <= today and diff.days < 300:
                return fecha
            else:
                raise forms.ValidationError(
                    u'La fecha de la ecografia no puede ser mayor a la '
                    'fecha actual ni mayor a 10 meses antes de la fecha actual')
        else:
            return fecha

    def clean_ila(self):
        ila = self.cleaned_data['ila']
        if ila:
            if 0 < ila < 1000:
                return ila
            else:
                raise forms.ValidationError(
                    u'Debe ser un valor numérico positivo de máximo 3 cifras')
        else:
            return ila

    '''
    def clean_biometria_fetal(self):
        biometria_fetal = self.cleaned_data['biometria_fetal']
        if biometria_fetal:
            if 0 < biometria_fetal < 1000:
                return biometria_fetal
            else:
                raise forms.ValidationError(
                    u'Debe ser un valor numérico positivo de 3 máximo cifras')
        else:
            return biometria_fetal
    '''

    class Meta:
        model = Ecografia
        exclude = (
            'embarazo', 'establecimiento', 'numero', 'diametro_biparietal',
            'longitud_cefalo_caudal')


class EcografiaDetalleForm(forms.ModelForm):
    eliminado = forms.CharField(widget=forms.HiddenInput(), required=False)  # forms.BooleanField(initial=False,

    # required= False)

    def __init__(self, *args, **kwargs):
        super(EcografiaDetalleForm, self).__init__(*args, **kwargs)

    class Meta:
        model = EcografiaDetalle
        exclude = ('created', 'modified')
        labels = {
            'biometria_fetal': u'',
            'eliminado': u'',
        }

    def get_eliminado(self):
        return self['eliminado'].value()

    def clean_biometria_fetal(self):

        biometria_fetal = self.cleaned_data['biometria_fetal']
        if self.get_eliminado():
            return biometria_fetal

        if biometria_fetal:
            if 0 < biometria_fetal < 1000:
                return biometria_fetal
            else:
                raise forms.ValidationError(
                    u'Debe ser un valor numérico positivo de 3 máximo cifras')
        else:
            return biometria_fetal


EcografiaDetalleFormSet = inlineformset_factory(Ecografia, EcografiaDetalle, form=EcografiaDetalleForm, min_num=1,
                                                max_num=5, extra=0)


class PlanPartoForm(forms.ModelForm):
    SI_NO_CHOICES = (
        (True, 'Si'),
        (False, 'No'),
        (None, '')
    )

    class Meta:
        model = PlanParto
        exclude = ('embarazo', 'establecimiento', 'edad_gestacional_elegida')

    def __init__(self, *args, **kwargs):
        super(PlanPartoForm, self).__init__(*args, **kwargs)
        self.fields['e1_lugar_atencion'].label = ''.join([
            '¿A decidido donde va ha atender su parto?'])
        self.fields['e1_lugar_atencion_otros'].label = 'Especificar'
        self.fields['e1_lugar_atencion_razon_eleccion'].label = ''.join([
            '¿Cuales son las razones para su elección?'])
