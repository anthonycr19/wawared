from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from controles.models import Control
from pacientes.models import Paciente


# Create your views here.
class ReportesTemplateView(TemplateView):
    template_name = 'gestantes/reportes.html'
    model = Paciente
    pk_url_kwarg = 'paciente_id'
    context_object_name = 'paciente'
    embarazo = None
    paciente_key = 'paciente_id'

    def get_context_data(self, **kwargs):
        context = super(ReportesTemplateView, self).get_context_data(**kwargs)
        paciente = Paciente.objects.get(numero_documento=self.request.user)
        context.update({
            'controles': Control.objects.filter(
                embarazo=self.embarazo).order_by('numero'),
            'embarazo': self.embarazo,
            'paciente': paciente
        })
        return context


def generar_reporte(request, *args, **kwargs):
    paciente = Paciente.objects.get(numero_documento=request.user)
    control = Control.objects.filter(paciente=paciente).latest('numero')
    return HttpResponseRedirect(reverse(
        'controles:reports:carne_control_prenatal',
        kwargs={'control_id': control.id}))
