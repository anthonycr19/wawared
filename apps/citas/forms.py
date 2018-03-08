from django import forms
from pacientes.models import Paciente
from .models import Cita


class CitaRegisterForm(forms.ModelForm):
    cita_fecha = forms.DateField(label=u'Fecha')
    cita_hora = forms.TimeField(label=u'Hora')

    def __init__(self, *args, **kwargs):
        super(CitaRegisterForm, self).__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Paciente.objects.none()
        self.fields['paciente'].widget = forms.HiddenInput()

    class Meta:
        model = Cita
        fields = ('paciente', 'comentario')


class CitaForm(forms.ModelForm):
    cita_fecha = forms.DateField(label=u'Fecha')
    cita_hora = forms.TimeField(label=u'Hora')

    class Meta:
        model = Cita
        fields = ('comentario',)
