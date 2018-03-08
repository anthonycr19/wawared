# coding: utf-8
from django.forms import TextInput
from cie.models import ICD10Base
from establecimientos.models import Establecimiento


class CIESelect(TextInput):

    def render(self, name, value, attrs=None):
        try:
            cie_name = ICD10Base.objects.get(id=value).nombre
        except (ICD10Base.DoesNotExist, ValueError):
            cie_name = ''
        attrs.update({
            'data-name': cie_name
        })
        return super(TextInput, self).render(name, value, attrs=attrs)


class EstablecimientoSelect(TextInput):

    def render(self, name, value, attrs=None):
        try:
            establecimiento_name = Establecimiento.objects.get(id=value).nombre
        except (Establecimiento.DoesNotExist, ValueError):
            establecimiento_name = ''
        attrs.update({
            'data-name': establecimiento_name
        })
        return super(TextInput, self).render(name, value, attrs=attrs)
