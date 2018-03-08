# Python imports


# Django imports


# Third party apps imports
from import_export.resources import ModelResource

# Local imports
from .models import ICD10Base


class ICD10BaseResource(ModelResource):
    class Meta:
        model = ICD10Base
        fields = ('id', 'codigo', 'nombre', 'nombre_mostrar')
        exclude = ('is_activo', 'is_familia', 'is_medico', 'is_icd10')
