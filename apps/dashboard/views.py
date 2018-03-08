from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from datetime import datetime, timedelta, time, date
import datetime

from citas.models import Cita
from common.views import LoginRequiredMixin
from establecimientos.models import Establecimiento
from pacientes.models import HistoriaClinica
from citas.citasminsa import CitasRest


class EstablecimientoRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if 'establecimiento_id' not in request.session:
            messages.info(
                request, u'Debe escoger un establecimiento para continuar')
            return HttpResponseRedirect(reverse('choose_establecimiento'))
        return super(EstablecimientoRequiredMixin, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EstablecimientoRequiredMixin, self).get_context_data(**kwargs)
        establecimiento_actual = Establecimiento.objects.get(id=self.request.session['establecimiento_id'])

        if 'modulo_control' in self.request.session:
            modulo_control = self.request.session['modulo_control']
        else:
            modulo_control = True

        if 'modulo_citas' in self.request.session:
            modulo_citas = self.request.session['modulo_citas']
        else:
            modulo_citas = False

        context.update({
            'establecimiento_actual': establecimiento_actual,
            'modulo_control': modulo_control,
            'modulo_citas': modulo_citas
        })

        return context


class HistoriaClinicaRequiredMixin(object):
    paciente_key = 'id'

    def dispatch(self, request, *args, **kwargs):
        if HistoriaClinica.objects.filter(
            establecimiento_id=request.session['establecimiento_id'],
            paciente_id=kwargs.get(self.paciente_key)).exists():
            return super(HistoriaClinicaRequiredMixin, self).dispatch(
                request, *args, **kwargs)
        else:
            messages.warning(
                request,
                u'No existe historia clinica registrada para la gestante '
                'en este establecimiento, debe crear una')
            return HttpResponseRedirect(
                reverse('paciente:historia_clinica_create', kwargs={
                    'paciente_id': kwargs.get(self.paciente_key)}))

    def get_context_data(self, **kwargs):
        context = super(HistoriaClinicaRequiredMixin, self).get_context_data(**kwargs)
        establecimiento_actual = Establecimiento.objects.get(id=self.request.session['establecimiento_id'])

        if 'modulo_control' in self.request.session:
            modulo_control = self.request.session['modulo_control']
        else:
            modulo_control = True

        if 'modulo_citas' in self.request.session:
            modulo_citas = self.request.session['modulo_citas']
        else:
            modulo_citas = False

        context.update({
            'establecimiento_actual': establecimiento_actual,
            'modulo_control': modulo_control,
            'modulo_citas': modulo_citas
        })
        return context


class DashboardHomeView(EstablecimientoRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def dispatch(self, request, *args, **kwargs):

        if 'modulo_control' in self.request.session:
            if not self.request.session['modulo_control']:
                return HttpResponseRedirect(reverse('partos:home'))

        return super(DashboardHomeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DashboardHomeView, self).get_context_data(**kwargs)
        establecimiento_actual = Establecimiento.objects.get(
            id=self.request.session['establecimiento_id'])

        if establecimiento_actual.modulo_citas:
            citas_rest = CitasRest()

            lista_citas = citas_rest.get_citas(establecimiento_actual, \
                                               self.request.user, datetime.datetime.now().strftime('%Y-%m-%d'))
        else:
            lista_citas = self.get_citas()

        context.update({
            'menu': 'inicio',
            'citas': lista_citas,
            'citas_vencidas': self.get_citas_vencidas(),
            'establecimientos': Establecimiento.objects.filter(
                diresa=establecimiento_actual.diresa)
        })
        return context

    def get_success_url(self):
        if 'modulo_control' in self.request.session:
            if self.request.session['modulo_control']:
                reverse('partos:home')
            else:
                reverse('dashboard_home')
        else:
            reverse('dashboard_home')

    def get_citas(self):

        establecimiento_actual = Establecimiento.objects.get(id=self.request.session['establecimiento_id'])
        if establecimiento_actual.is_sistema_externo_admision:
            return Cita.get_citas_programadas_for_medical_specialist(
                self.request.session['establecimiento_id'], self.request.user)
        else:
            return Cita.get_citas_programadas(
                self.request.session['establecimiento_id'])

    def get_citas_vencidas(self):
        establecimiento_actual = Establecimiento.objects.get(id=self.request.session['establecimiento_id'])
        if establecimiento_actual.is_sistema_externo_admision:
            return Cita.get_citas_vencidas_for_medical_specialist(
                self.request.session['establecimiento_id'], self.request.user)
        else:
            return Cita.get_citas_vencidas(
                self.request.session['establecimiento_id'])
