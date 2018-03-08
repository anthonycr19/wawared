from django import template

from pacientes.models import HistoriaClinica

register = template.Library()


@register.filter(name='hc')
def get_hc(paciente, request):
    try:
        hc = HistoriaClinica.objects.get(
            paciente=paciente,
            establecimiento_id=request.session['establecimiento_id'])
        return hc.numero
    except HistoriaClinica.DoesNotExist:
        return 'NE'
