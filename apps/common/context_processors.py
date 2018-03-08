from django.conf import settings


def boolean_variables(request):
    return {
        'True': True,
        'False': False,
        'None': None
    }


def capacitacion(request):
    return {
        'capacitacion': settings.CAPACITACION
    }
