from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from ciudadano import CiudadanoRest


class PacienteManager(models.Manager):
    def get(self, *args, **kwargs):
        try:
            resultado = super(PacienteManager, self).get(*args, **kwargs)
        except ObjectDoesNotExist as e:
            if 'numero_documento' in kwargs:

                if not 'tipo_documento' in kwargs:
                    return None

                if kwargs['tipo_documento'] == 'dni':
                    paciente = CiudadanoRest().get_persona_por_dni(kwargs['numero_documento'])

                    if paciente:
                        try:
                            paciente.save()
                            resultado = paciente
                        except Exception as e:
                            return None
                    else:
                        resultado = None
                else:
                    resultado = None

        return resultado;
