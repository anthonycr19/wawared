# coding: utf-8
import json
from datetime import datetime

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, UpdateView, RedirectView, View, TemplateView, ListView
from django.db import transaction

from partos.models import TerminacionEmbarazo, Ingreso
from establecimientos.models import Establecimiento
from pacientes.models import Paciente
from cie.models import ICD10
from puerperio import reports
from controles.models import DiagnosticoDetalle
from .models import Monitoreo, MonitoreoMedicion, EgresoRecienNacido, EgresoGestante, RecienNacido, TerminacionPuerpera
from .forms import MonitoreoMedicionForm, EgresoRecienNacidoForm, EgresoGestanteForm, RecienNacidoForm, TerminacionPuerperaForm
from pacientes.views import PacienteSearchView
from dashboard.views import EstablecimientoRequiredMixin


class HomeView(EstablecimientoRequiredMixin, ListView):

    template_name = 'puerperio/home.html'
    model = Ingreso
    paginate_by = 10
    context_object_name = 'ingresos'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context.update({
            'terminaciones_embarazo': TerminacionEmbarazo.objects.filter(
                    establecimiento_id=self.request.session['establecimiento_id']).exclude(
                        id__in=TerminacionPuerpera.objects.all().values_list(
                            'terminacion_embarazo__id', flat=True))
        })
        return context


class PPacienteSearchView(PacienteSearchView):
    template_name = 'puerperio/paciente_list.html'


class RecienNacidoMixin(object):

    terminacion_embarazo = None
    object = None

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        egreso_form = EgresoRecienNacidoForm(
            request.POST or None, prefix='egreso', instance=self.get_egreso())
        if form.is_valid():
            if form.cleaned_data['tiene_egreso'] and not egreso_form.is_valid():
                return self.form_invalid(form, egreso_form)
            else:
                return self.form_valid(form, egreso_form)
        else:
            return self.form_invalid(form, egreso_form)

    def get_form(self, form_class):
        return form_class(self.request.POST or None, instance=self.get_object())

    def form_valid(self, form, egreso_form):
        try:
            with transaction.atomic():

                recien_nacido = form.save(commit=False)

                if not form.instance.id:
                    recien_nacido.terminacion_embarazo = self.terminacion_embarazo
                    recien_nacido.creator = self.request.user

                recien_nacido.modifier = self.request.user
                recien_nacido.save()

                if egreso_form.is_valid():
                    egreso = egreso_form.save(commit=False)
                    egreso.establecimiento_id = self.request.session['establecimiento_id']

                    if not egreso_form.instance.id:
                        egreso.recien_nacido = recien_nacido
                        egreso.creator = self.request.user

                    egreso.modifier = self.request.user
                    egreso.save()

            return super(RecienNacidoMixin, self).form_valid(form)
        except Exception as e:
            # TODO: add logger here
            messages.error(self.request, 'Ocurrio un error vuelva a intentarlo')
            return self.form_invalid(form, egreso_form)

    def form_invalid(self, form, egreso_form):
        return self.render_to_response(self.get_context_data(form=form, egreso_form=egreso_form))

    def get_context_data(self, **kwargs):
        context = super(RecienNacidoMixin, self).get_context_data(**kwargs)
        context.update({
            'paciente': self.terminacion_embarazo.paciente,
            'terminacion_embarazo': self.terminacion_embarazo
        })
        if 'egreso_form' not in kwargs:
            context.update({
                'egreso_form': EgresoRecienNacidoForm(None, instance=self.get_egreso(), prefix='egreso')
            })
        return context

    def get_egreso(self):
        raise NotImplementedError


class RecienNacidoCreateView(EstablecimientoRequiredMixin, RecienNacidoMixin, CreateView):

    template_name = 'puerperio/recien_nacido_create.html'
    model = RecienNacido
    form_class = RecienNacidoForm
    terminacion_embarazo = None

    def dispatch(self, request, *args, **kwargs):
        self.terminacion_embarazo = get_object_or_404(
            TerminacionEmbarazo, id=kwargs.get('terminacion_embarazo_id'))
        return super(RecienNacidoCreateView, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class):
        form = super(RecienNacidoMixin, self).get_form(form_class)
        # TODO: agregar apellidos del padre
        form.fields[
            'apellido_paterno'].initial = self.terminacion_embarazo.paciente.apellido_paterno
        form.fields[
            'apellido_materno'].initial = self.terminacion_embarazo.paciente.apellido_materno
        return form

    def get_egreso(self):
        return EgresoRecienNacido()

    def get_context_data(self, **kwargs):
        context = super(
            RecienNacidoCreateView, self).get_context_data(**kwargs)
        context.update({
            'ingreso': self.terminacion_embarazo.ingreso
        })
        return context

    def get_success_url(self):
        messages.success(self.request, 'Recien nacido registrado')
        return reverse('puerperio:resume', kwargs={'terminacion_embarazo_id': self.terminacion_embarazo.id})


class RecienNacidoUpdateView(EstablecimientoRequiredMixin, RecienNacidoMixin, UpdateView):

    template_name = 'puerperio/recien_nacido_edit.html'
    model = RecienNacido
    form_class = RecienNacidoForm
    terminacion_embarazo = None
    pk_url_kwarg = 'recien_nacido_id'

    def dispatch(self, request, *args, **kwargs):
        self.terminacion_embarazo = get_object_or_404(TerminacionEmbarazo, id=kwargs.get('terminacion_embarazo_id'))
        return super(RecienNacidoUpdateView, self).dispatch(request, *args, **kwargs)

    def get_egreso(self):
        obj = self.get_object()
        if hasattr(obj, 'egreso') and obj.egreso.id:
            return obj.egreso
        else:
            return EgresoRecienNacido()

    def get_context_data(self, **kwargs):
        context = super(RecienNacidoUpdateView, self).get_context_data(**kwargs)
        context.update({
            'ingreso': self.terminacion_embarazo.ingreso
        })
        return context

    def get_success_url(self):
        messages.success(self.request, 'Recien nacido actualizado')
        return reverse('puerperio:resume', kwargs={'terminacion_embarazo_id': self.terminacion_embarazo.id})


class ResumeView(EstablecimientoRequiredMixin, TemplateView):

    template_name = 'puerperio/resume.html'
    terminacion_embarazo = None

    def dispatch(self, request, *args, **kwargs):
        self.terminacion_embarazo = get_object_or_404(TerminacionEmbarazo, id=kwargs.get('terminacion_embarazo_id'))
        return super(ResumeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ResumeView, self).get_context_data(**kwargs)
        context.update({
            'paciente': self.terminacion_embarazo.paciente,
            'recien_nacidos': self.terminacion_embarazo.recien_nacidos.all(),
            'terminacion_embarazo': self.terminacion_embarazo,
            'ingreso': self.terminacion_embarazo.ingreso
        })
        return context


class MonitoreoView(EstablecimientoRequiredMixin, CreateView):

    template_name = 'puerperio/monitoreo.html'
    model = MonitoreoMedicion
    form_class = MonitoreoMedicionForm
    terminacion_embarazo = None

    def dispatch(self, request, *args, **kwargs):
        self.terminacion_embarazo = get_object_or_404(
            TerminacionEmbarazo, id=self.kwargs.get('terminacion_embarazo_id'))
        return super(MonitoreoView, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class):
        form = super(MonitoreoView, self).get_form(form_class)
        form.fields['fecha'].initial = datetime.today().date()
        return form

    def get_context_data(self, **kwargs):
        context = super(MonitoreoView, self).get_context_data(**kwargs)
        context.update({
            'terminacion_embarazo': self.terminacion_embarazo,
            'monitoreo': self._get_monitoreo(),
            'ingreso': self.terminacion_embarazo.ingreso
        })
        return context

    def form_valid(self, form):
        medicion = form.save(commit=False)
        medicion.establecimiento_id = self.request.session['establecimiento_id']
        medicion.creator = self.request.user
        medicion.modifier = self.request.user
        medicion.monitoreo = self._get_monitoreo()
        return super(MonitoreoView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Se registro el monitoreo')
        return reverse('puerperio:monitoreo', kwargs={'terminacion_embarazo_id': self.terminacion_embarazo.id})

    def _get_monitoreo(self):
        values = {
            'paciente': self.terminacion_embarazo.paciente,
            'terminacion_embarazo': self.terminacion_embarazo
        }
        try:
            monitoreo = Monitoreo.objects.get(**values)
        except Monitoreo.DoesNotExist:
            monitoreo = Monitoreo(**values)
            monitoreo.establecimiento_id = self.request.session['establecimiento_id']
            monitoreo.embarazo = self.terminacion_embarazo.ingreso.embarazo
            monitoreo.creator = self.request.user
            monitoreo.modifier = self.request.user
            monitoreo.save()
        return monitoreo


class MonitoreoMedicionUpdateView(EstablecimientoRequiredMixin, UpdateView):

    template_name = 'puerperio/monitoreo.html'
    model = MonitoreoMedicion
    pk_url_kwarg = 'medicion_id'
    context_object_name = 'medicion'
    form_class = MonitoreoMedicionForm
    terminacion_embarazo = None

    def dispatch(self, request, *args, **kwargs):
        self.terminacion_embarazo = get_object_or_404(
            TerminacionEmbarazo, id=self.kwargs.get('terminacion_embarazo_id'))
        return super(MonitoreoMedicionUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MonitoreoMedicionUpdateView, self).get_context_data(**kwargs)
        context.update({
            'terminacion_embarazo': self.terminacion_embarazo,
            'monitoreo': self._get_monitoreo(),
            'update_medicion': True,
            'ingreso': self.terminacion_embarazo.ingreso
        })
        return context

    def get_success_url(self):
        messages.success(self.request, 'Se actualizó el monitoreo')
        return reverse('puerperio:monitoreo', kwargs={'terminacion_embarazo_id': self.terminacion_embarazo.id})

    def _get_monitoreo(self):
        terminacion_embarazo = self.terminacion_embarazo
        values = {
            'paciente': terminacion_embarazo.paciente,
            'terminacion_embarazo': terminacion_embarazo
        }
        try:
            monitoreo = Monitoreo.objects.get(**values)
        except Monitoreo.DoesNotExist:
            monitoreo = Monitoreo(**values)
            monitoreo.creator = self.request.user
            monitoreo.modifier = self.request.user
            monitoreo.save()
        return monitoreo


class EgresoGestanteView(EstablecimientoRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        terminacion_embarazo = get_object_or_404(TerminacionEmbarazo, id=kwargs.get('terminacion_embarazo_id'))
        egreso = EgresoGestante.objects.filter(terminacion_embarazo=terminacion_embarazo).first()
        if egreso:
            return reverse('puerperio:egreso_gestante_edit',
                           kwargs={'terminacion_embarazo_id': terminacion_embarazo.id})
        else:
            return reverse('puerperio:egreso_gestante_create',
                           kwargs={'terminacion_embarazo_id': terminacion_embarazo.id})


class EgresoGestanteCreateView(EstablecimientoRequiredMixin, CreateView):

    model = EgresoGestante
    form_class = EgresoGestanteForm
    template_name = 'puerperio/egreso_gestante.html'
    terminacion_embarazo = None

    def dispatch(self, request, *args, **kwargs):
        self.terminacion_embarazo = get_object_or_404(TerminacionEmbarazo, id=kwargs.get('terminacion_embarazo_id'))
        if self.model.objects.filter(terminacion_embarazo=self.terminacion_embarazo).exists():
            messages.warning(request, 'Ya se registro un egreso para la paciente')
            return HttpResponseRedirect(reverse('puerperio:resume',
                                                kwargs={'terminacion_embarazo_id': self.terminacion_embarazo.id}))
        return super(EgresoGestanteCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        egreso = form.save(commit=False)
        egreso.establecimiento_id = self.request.session['establecimiento_id']
        egreso.creator = self.request.user
        egreso.modifier = self.request.user
        egreso.paciente = self.terminacion_embarazo.paciente
        egreso.terminacion_embarazo = self.terminacion_embarazo
        egreso.ingreso = self.terminacion_embarazo.ingreso
        egreso.save()
        return super(EgresoGestanteCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EgresoGestanteCreateView, self).get_context_data(**kwargs)
        context.update({
            'terminacion_embarazo': self.terminacion_embarazo,
            'ingreso': self.terminacion_embarazo.ingreso
        })
        return context

    def get_success_url(self):
        messages.success(self.request, u'Se registró el egreso del la paciente')
        return reverse('puerperio:resume', kwargs={'terminacion_embarazo_id': self.terminacion_embarazo.id})


class EgresoGestanteUpdateView(EstablecimientoRequiredMixin, UpdateView):

    model = EgresoGestante
    form_class = EgresoGestanteForm
    template_name = 'puerperio/egreso_gestante.html'
    terminacion_embarazo = None
    object = None

    def dispatch(self, request, *args, **kwargs):
        self.terminacion_embarazo = get_object_or_404(TerminacionEmbarazo, id=kwargs.get('terminacion_embarazo_id'))
        return super(EgresoGestanteUpdateView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if self.object is None:
            try:
                self.object = self.model.objects.get(terminacion_embarazo=self.terminacion_embarazo)
            except self.model.DoesNotExist:
                raise Http404
        return self.object

    def form_valid(self, form):
        egreso = form.save(commit=False)
        egreso.modifier = self.request.user
        egreso.save()
        return super(EgresoGestanteUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EgresoGestanteUpdateView, self).get_context_data(**kwargs)
        context.update({
            'terminacion_embarazo': self.terminacion_embarazo,
            'ingreso': self.terminacion_embarazo.ingreso
        })
        return context

    def get_success_url(self):
        messages.success(self.request, u'Se actualizó el egreso de la paciente')
        return reverse('puerperio:resume', kwargs={'terminacion_embarazo_id': self.terminacion_embarazo.id})

    def get_cies(self):
        codes = ['59430', '99402', 'Z391', '99403', 'Z392', 'Z298']
        return ICD10.objects.filter(codigo__in=codes)


class EpicrisisReportView(View):

    def get(self, request, *args, **kwargs):
        egreso = get_object_or_404(EgresoGestante, id=kwargs.get('egreso_gestante_id', ''))
        report = reports.EpicrisisReport(egreso)
        return report.render_to_response()


class TerminacionPuerperaView(EstablecimientoRequiredMixin, CreateView):
    model = TerminacionPuerpera
    form_class = TerminacionPuerperaForm
    template_name = 'puerperio/cierre_puerperio.html'
    terminacion_embarazo = None
    object = None

    def dispatch(self, request, *args, **kwargs):
        self.terminacion_embarazo = get_object_or_404(TerminacionEmbarazo, id=kwargs.get('terminacion_embarazo_id'))
        if self.model.objects.filter(terminacion_embarazo=self.terminacion_embarazo).exists():
            messages.warning(request, 'Ya se registro un cierre de puerperio')
            return HttpResponseRedirect(reverse('puerperio:home'))
        return super(TerminacionPuerperaView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.object

    def form_valid(self, form):
        egreso = form.save(commit=False)
        egreso.establecimiento_id = self.request.session['establecimiento_id']
        egreso.creator = self.request.user
        egreso.modifier = self.request.user
        egreso.paciente = self.terminacion_embarazo.paciente
        egreso.terminacion_embarazo = self.terminacion_embarazo
        egreso.ingreso = self.terminacion_embarazo.ingreso
        egreso.monitoreo = self.get_monitoreo()
        egreso.monitoreo.status = Monitoreo.CERRADO
        egreso.monitoreo.save()
        egreso.save()
        cies = DiagnosticoDetalle.objects.filter(diagnostico_embarazo=self.terminacion_embarazo)
        if cies:
            for cie in cies:
                cie.diagnostico_puerperio = egreso
                cie.save()
        return super(TerminacionPuerperaView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TerminacionPuerperaView, self).get_context_data(**kwargs)
        detalles = self.terminacion_embarazo.detalles_puerperio.all()
        cies = self.get_cies()
        cies = cies.exclude(
            id__in=[detalle.cie.id for detalle in detalles]).order_by('nombre')
        _cies = []
        for cie in cies:
            _cies.append({
                'id': cie.id,
                'nombre': cie.nombre,
                'nombre_mostrar': cie.nombre_mostrar,
                'codigo': cie.codigo,
                'nombre_display': cie.nombre_display
            })
        cies = _cies
        context.update({
            'terminacion_embarazo': self.terminacion_embarazo,
            'detalles': detalles,
            'cies': cies,
            'ingreso': self.terminacion_embarazo.ingreso
        })
        return context

    def get_success_url(self):
        messages.success(self.request, u'Se registró el cierre de puerperio')
        return reverse('puerperio:home')

    def get_cies(self):
        codes = ['59430', '99402', 'Z391', '99403', 'Z392', 'Z298']
        return ICD10.objects.filter(codigo__in=codes)

    def get_monitoreo(self):
        monitoreo = Monitoreo.objects.get(terminacion_embarazo=self.terminacion_embarazo)
        return monitoreo

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            try:
                data = json.loads(request.body)
                for item in data["cie"]:
                    cie = ICD10.objects.get(codigo=item['codigo'])
                    detalle = DiagnosticoDetalle.objects.filter(cie=cie,
                                                                diagnostico_embarazo=self.terminacion_embarazo).first()
                    if not detalle:
                        detalle = DiagnosticoDetalle.objects.create(cie=cie,
                                                                    diagnostico_embarazo=self.terminacion_embarazo,
                                                                    created_by=request.user, order=0)
                    if item['delete']:
                        detalle.delete()
                    else:
                        detalle.observacion = item['observacion']
                        detalle.order = item.get('order', 0)
                        detalle.tipo = item['tipo'].upper()
                        detalle.laboratorio = item['laboratorio']
                        detalle.save()
                        print("salva")

                response_data = {'status': 'success'}
            except ValueError:
                response_data = {'status': 'failed'}

            return JsonResponse(response_data)
        else:
            return super(TerminacionPuerperaView, self).post(request, *args, **kwargs)
