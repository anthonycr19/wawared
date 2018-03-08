# Python imports


# Django imports


# Third party apps imports
from import_export.resources import ModelResource

# Local imports
from .models import Diresa, Red, Microred, Establecimiento


class DiresaResource(ModelResource):
    class Meta:
        model = Diresa
        fields = ('id', 'nombre', 'codigo',)
        exclude = ('logo',)


class RedResource(ModelResource):
    class Meta:
        model = Red
        fields = ('id', 'diresa', 'nombre',)
        exclude = ('estado', 'logo',)


class MicroredResource(ModelResource):
    class Meta:
        model = Microred
        fields = ('id', 'red', 'nombre',)
        exclude = ('estado', 'numero',)


class EstablecimientoResource(ModelResource):
    class Meta:
        model = Establecimiento
        fields = (
            'id', 'diresa', 'red', 'microred', 'nombre', 'codigo_renaes',
            'disa', 'codigo_his',)
        exclude = ('logo', 'descripcion', 'telefono', 'lote',)
