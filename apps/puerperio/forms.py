# coding: utf-8
from django import forms
from cie.models import ICD10Base
from establecimientos.models import Establecimiento
from dashboard.widgets import CIESelect, EstablecimientoSelect

from .models import MonitoreoMedicion, EgresoRecienNacido, EgresoGestante, RecienNacido, TerminacionPuerpera


class MonitoreoMedicionForm(forms.ModelForm):

    class Meta:
        model = MonitoreoMedicion
        exclude = ('establecimiento', 'monitoreo', 'modifier', 'creator')


class RecienNacidoForm(forms.ModelForm):

    class Meta:
        model = RecienNacido
        exclude = ('terminacion_embarazo', 'creator', 'modifier')


class EgresoGestanteForm(forms.ModelForm):

    diagnostico = forms.CharField(
        label='Diagnostico', required=True, widget=CIESelect)
    diagnostico_traslado = forms.CharField(
        label='Diagnostico traslado', required=False, widget=CIESelect)
    diagnostico_fallecimiento = forms.CharField(
        label='Diagnostico fallecimiento', required=False, widget=CIESelect)

    def clean_diagnostico(self):
        try:
            cie = ICD10Base.objects.get(id=self.cleaned_data['diagnostico'])
        except (ICD10Base.DoesNotExist, ValueError):
            raise forms.ValidationError('CIE no existe')
        return cie

    def clean_diagnostico_traslado(self):
        try:
            cie = ICD10Base.objects.get(
                id=self.cleaned_data['diagnostico_traslado'])
        except ICD10Base.DoesNotExist:
            raise forms.ValidationError('CIE no existe')
        except ValueError:
            return None
        return cie

    def clean_diagnostico_fallecimiento(self):
        try:
            cie = ICD10Base.objects.get(
                id=self.cleaned_data['diagnostico_fallecimiento'])
        except ICD10Base.DoesNotExist:
            raise forms.ValidationError('CIE no existe')
        except ValueError:
            return None
        return cie

    class Meta:
        model = EgresoGestante
        exclude = ('establecimiento', 'paciente',
                   'terminacion_embarazo', 'ingreso', 'modifier', 'creator')


class EgresoRecienNacidoForm(forms.ModelForm):

    diagnostico = forms.CharField(
        label='Diagnostico', required=True, widget=CIESelect)
    diagnostico_traslado = forms.CharField(
        label='Diagnostico traslado', required=False, widget=CIESelect)
    diagnostico_fallecimiento = forms.CharField(
        label='Diagnostico fallecimiento', required=False, widget=CIESelect)

    cui = forms.ChoiceField(
        label='CUI', choices=EgresoRecienNacido.SI_NO_CHOICES, widget=forms.RadioSelect, initial=False)
    seguro = forms.ChoiceField(
        label='Seguro', choices=EgresoRecienNacido.SI_NO_CHOICES, widget=forms.RadioSelect, initial=False)

    tn_tsh = forms.ChoiceField(
        label='TSH', choices=EgresoRecienNacido.SI_NO_CHOICES, widget=forms.RadioSelect, initial=False)
    tn_fibrosis = forms.ChoiceField(
        label='Fibrosis Quistica', choices=EgresoRecienNacido.SI_NO_CHOICES, widget=forms.RadioSelect, initial=False)
    tn_fenilceto = forms.ChoiceField(
        label='Fenilceto nuria', choices=EgresoRecienNacido.SI_NO_CHOICES, widget=forms.RadioSelect, initial=False)
    tn_hiperplasia = forms.ChoiceField(
        label='Hiperplasia Suprarrenal', choices=EgresoRecienNacido.SI_NO_CHOICES, widget=forms.RadioSelect, initial=False)

    def clean_diagnostico(self):
        try:
            cie = ICD10Base.objects.get(id=self.cleaned_data['diagnostico'])
        except (ICD10Base.DoesNotExist, ValueError):
            raise forms.ValidationError('CIE no existe')
        return cie

    def clean_diagnostico_traslado(self):
        try:
            cie = ICD10Base.objects.get(
                id=self.cleaned_data['diagnostico_traslado'])
        except ICD10Base.DoesNotExist:
            raise forms.ValidationError('CIE no existe')
        except ValueError:
            return None
        return cie

    def clean_diagnostico_fallecimiento(self):
        try:
            cie = ICD10Base.objects.get(
                id=self.cleaned_data['diagnostico_fallecimiento'])
        except ICD10Base.DoesNotExist:
            raise forms.ValidationError('CIE no existe')
        except ValueError:
            return None
        return cie

    class Meta:
        model = EgresoRecienNacido
        exclude = ('establecimiento', 'recien_nacido', 'modifier', 'creator')


class TerminacionPuerperaForm(forms.ModelForm):

    centro_salud = forms.CharField(
        label='Centro de salud perteneciente', required=True, widget=EstablecimientoSelect)

    def clean_centro_salud(self):
        try:
            establecimiento = Establecimiento.objects.get(
                id=self.cleaned_data['centro_salud'])
        except (Establecimiento.DoesNotExist, ValueError):
            raise forms.ValidationError('Establecimiento no existe')
        return establecimiento

    class Meta:
        model = TerminacionPuerpera
        exclude = ('establecimiento', 'paciente', 'monitoreo',
                   'terminacion_embarazo', 'ingreso', 'modifier', 'creator')
