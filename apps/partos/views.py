# coding: utf-8
from __future__ import unicode_literals
from collections import namedtuple, defaultdict
from datetime import datetime, timedelta, time
from inspect import getmembers
import json

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.db import transaction, IntegrityError
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, UpdateView, DetailView, View, FormView

from common.views import PdfView
from partos import reports
from cie.models import ICD10
from dashboard.views import EstablecimientoRequiredMixin
from embarazos.models import Embarazo, Ecografia, UltimoEmbarazo
from pacientes.models import Paciente, HistoriaClinica
from controles.models import Laboratorio, Sintoma, ExamenFisico, Control, ExamenFisicoFetal
from controles.forms import LaboratorioForm, ControlForm, ExamenFetalFormSet, ExamenFetalMedicionFormSet
from pacientes.views import (
    PacienteDetailView, PacienteUpdateView, PacienteCreateView, PacienteSearchView,
                             PacienteCreateForce, PacienteAntecedentesDetailView, PacienteAntecedentesUpdateView,
                             AntecedentesFamiliaresView, AntecedentesMedicosView, PacienteControlUpdateView)
from embarazos.views import (
    EmbarazoCreateView, EcografiasView, EcografiaCreateView, EcografiaUpdateView,
                             EcografiaDeleteView, UltimoEmbarazoCreateView, UltimosEmbarazosView, UltimoEmbarazoUpdateView,
                             UltimoEmbarazoDeleteView, EmbarazoUpdateCurrentView)
from puerperio.models import MonitoreoMedicion
from .models import Ingreso, Partograma, PartogramaMedicion, TerminacionEmbarazo, Placenta
from .forms import IngresoForm, PartogramaMedicionForm, TerminacionEmbarazoForm, ExamenFisicoIngresoForm, PlacentaFormSet
from pacientes.ciudadano import CiudadanoRest
from establecimientos.models import Establecimiento
from django.conf import settings

User = get_user_model()


class HomeView(EstablecimientoRequiredMixin, ListView):
    template_name = 'partos/home.html'
    model = Ingreso
    paginate_by = 10
    context_object_name = 'ingresos'

    def get_queryset(self):
        qs = super(HomeView, self).get_queryset()
        qs = qs.filter(establecimiento_id=self.request.session[
                       'establecimiento_id']).filter(terminacion_embarazo=None)
        return qs

    def traer_hc(self):
        establecimiento_id = self.request.session['establecimiento_id']
        return HistoriaClinica.objects.get(establecimiento_id=establecimiento_id, paciente_id=1).numero


class IngresoCreateView(EstablecimientoRequiredMixin, CreateView):
    template_name = 'partos/ingreso.html'
    model = Ingreso
    form_class = IngresoForm
    paciente = None
    embarazo = None

    def dispatch(self, request, *args, **kwargs):
        self.embarazo = self._get_paciente().get_embarazo_actual()
        if self.embarazo is None:
            # crear un embarazo activo.
            messages.warning(
                request, u'No existe un embarazo activo, debe crear uno primero')
            return HttpResponseRedirect(reverse('partos:embarazo_create', kwargs={'paciente_id': self.paciente.id}))
        if hasattr(self.embarazo, 'ingreso') and self.embarazo.ingreso:
            messages.warning(request, 'Ya existe un ingreso registrado')
            return HttpResponseRedirect(reverse('partos:ingreso_edit', kwargs={'ingreso_id': self.embarazo.ingreso.id}))
        return super(IngresoCreateView, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class):
        form = super(IngresoCreateView, self).get_form(form_class)
        form.fields['fecha'].initial = datetime.today().date()
        form.fields['hora'].initial = datetime.today().time()
        form.fields['peso'].initial = None
        form.fields['imc'].initial = None
        last_control = self.embarazo.controles.last()
        if last_control is not None:
            form.fields['eg_elegida'].initial = last_control.eg_elegida
        return form

    def form_valid(self, form):
        ingreso = form.save(commit=False)
        ingreso.establecimiento_id = self.request.session['establecimiento_id']
        ingreso.paciente = self._get_paciente()
        ingreso.embarazo = self.embarazo
        ingreso.created_by = self.request.user
        ingreso.save()
        fcfs = ExamenFetalFormSet(self.request.POST, instance=self.object)
        if fcfs.is_valid():
            fcfs.instance = form.save()
            fcfs.ingres_partogama = ingreso
            fcfs.save()

        messages.success(
            self.request, 'Se registro el ingreso de {}'.format(ingreso.paciente.nombre_completo))
        return super(IngresoCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(IngresoCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['fcfs'] = ExamenFetalFormSet(self.request.POST)
        else:
            context['fcfs'] = ExamenFetalFormSet()
        context.update({
            'paciente': self._get_paciente(),
            'embarazo': self.embarazo,

        })
        return context

    def get_success_url(self):
        return reverse('partos:home')

    def _get_paciente(self):
        if self.paciente is not None:
            return self.paciente
        self.paciente = get_object_or_404(
            Paciente, id=self.kwargs.get('paciente_id', None))
        return self.paciente


class IngresoUpdateView(EstablecimientoRequiredMixin, UpdateView):
    template_name = 'partos/ingreso.html'
    model = Ingreso
    form_class = IngresoForm
    pk_url_kwarg = 'ingreso_id'

    def form_valid(self, form):
        ingreso = form.save(commit=False)
        ingreso.modifier = self.request.user
        ingreso.save()
        fcfs = ExamenFetalFormSet(self.request.POST, instance=self.object)
        if fcfs.is_valid():
            fcfs.save()
        messages.success(self.request, 'ingreso actualizado')
        return super(IngresoUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(IngresoUpdateView, self).get_context_data(**kwargs)
        context['fcfs'] = ExamenFetalFormSet(
            queryset=ExamenFisicoFetal.objects.filter(ingreso_parto=self.object.id), instance=self.object)
        context.update({
            'paciente': self.object.paciente,
            'embarazo': self.object.embarazo
        })
        return context

    def get_success_url(self):
        return reverse('partos:home')


class PPacienteDetailView(PacienteDetailView):
    template_name = 'partos/paciente_edit.html'


class PPacienteUpdateView(PacienteUpdateView):
    template_name = 'partos/paciente_edit.html'

    def get_success_url(self):
        messages.success(self.request, u'Los datos de la gestante fueron actualizados')
        return reverse('partos:paciente_antecedentes_edit', kwargs={'id': self.object.id})


class PPacienteControlUpdateView(PacienteControlUpdateView):
    template_name = 'partos/paciente_control_edit.html'

    def get_success_url(self):
        messages.success(self.request, u'Los datos de la gestante fueron actualizados')
        return reverse('paciente:control_antecedentes_edit', kwargs={'id': self.object.id})


class PEmbarazoCreateView(EmbarazoCreateView):
    template_name = 'partos/embarazo_register.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            paciente = Paciente.objects.get(id=kwargs.get('paciente_id', None))
            self.paciente = paciente
            self.object = self.model()
            try:
                Embarazo.objects.get(paciente=self.paciente, activo=True)
                return HttpResponseRedirect(reverse('partos:update_current', kwargs={'paciente_id': self.paciente.id}))
            except Embarazo.DoesNotExist:
                return super(PEmbarazoCreateView, self).dispatch(request, *args, **kwargs)
        except Paciente.DoesNotExist:
            raise Http404

    def form_valid(self, form, ficha_form, ficha_problema_form):
        embarazo = form.save(commit=False)
        embarazo.numero_cigarros_diarios = 0
        return super(PEmbarazoCreateView, self).form_valid(form, ficha_form, ficha_problema_form)

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse('partos:ingreso_register', kwargs={'paciente_id': self.paciente.id})


class PEmbarazoUpdateCurrentView(EmbarazoUpdateCurrentView):
    template_name = 'partos/embarazo_edit.html'

    def dispatch(self, request, *args, **kwargs):
        try:  # TODO DRY this
            paciente = Paciente.objects.get(id=kwargs.get('paciente_id', None))
            self.paciente = paciente
            try:
                self.object = Embarazo.objects.get(paciente=self.paciente, activo=True)
                return super(PEmbarazoUpdateCurrentView, self).dispatch(
                    request, *args, **kwargs)
            except Embarazo.DoesNotExist:
                messages.warning(
                    request, u'No existe un embarazo activo, debe crear uno primero')
                return HttpResponseRedirect(reverse(
                    'partos:embarazos_create', kwargs={'paciente_id': self.paciente.id}))
        except Paciente.DoesNotExist:
            raise Http404

    def get_success_url(self):
        messages.success(self.request, u'Se actualizó el embarazo')
        return reverse('partos:ingreso_register', kwargs={'paciente_id': self.paciente.id})


class PPacienteCreateView(PacienteCreateView):
    template_name = 'partos/paciente_register.html'

    def get_success_url(self):
        messages.success(self.request, u'Gestante registrada')
        return reverse('partos:paciente_antecedentes', kwargs={'id': self.object.id})


class PPacienteCreateForceView(EstablecimientoRequiredMixin, FormView):

    def get(self, request, *args, **kwargs):

        dni = kwargs['id']

        paciente = Paciente.objects.filter(
            tipo_documento='dni', numero_documento=dni).first()

        if paciente is None:
            paciente = CiudadanoRest().get_persona_por_dni(dni)
            paciente.save()

        try:
            hc = HistoriaClinica.objects.get(
                establecimiento=Establecimiento.objects.get(id=self.request.session['establecimiento_id']), numero=dni)
        except Exception as e:
            hc = HistoriaClinica()
            hc.numero = dni
            establecimiento = Establecimiento.objects.get(
                id=self.request.session['establecimiento_id'])
            hc.establecimiento = establecimiento

        hc.paciente = paciente
        hc.save()

        return HttpResponseRedirect(reverse('partos:paciente_update', kwargs={'id': paciente.id}))


class PPacienteSearchView(PacienteSearchView):
    template_name = 'partos/paciente_list.html'


class PPacienteAntecedentesDetailView(PacienteAntecedentesDetailView):
    template_name = 'partos/antecedentes.html'


class PPacienteAntecedentesUpdateView(PacienteAntecedentesUpdateView):
    template_name = 'partos/antecedentes.html'

    def get_success_url(self):
        messages.success(self.request, u'Se actualizaron los antecedentes ginecologicos')
        return reverse('partos:embarazo_create', kwargs={'paciente_id': self.paciente.id})


class PAntecedentesFamiliaresView(AntecedentesFamiliaresView):
    template_name = 'partos/antecedentes_familiares_edit.html'


class PAntecedentesMedicosView(AntecedentesMedicosView):
    template_name = 'partos/antecedentes_medicos_edit.html'


class PUltimosEmbarazosView(UltimosEmbarazosView):
    template_name = 'partos/ultimos_embarazos.html'


class PUltimoEmbarazoCreateView(UltimoEmbarazoCreateView):
    template_name = 'partos/ultimo_embarazo.html'


class PUltimoEmbarazoUpdateView(UltimoEmbarazoUpdateView):
    template_name = 'partos/ultimo_embarazo.html'


class PUltimoEmbarazoDeleteView(UltimoEmbarazoDeleteView):
    template_name = 'partos/ultimo_embarazo.html'

    def get_redirect_url(self, *args, **kwargs):
        ue = get_object_or_404(UltimoEmbarazo, id=kwargs.get('id', 0))
        if ue.created.date() < datetime.today().date():
            messages.warning(self.request, 'No puede eliminar embarazo anterior')
            return reverse('partos:embarazos_ultimos_embarazos', kwargs={'paciente_id': self.paciente.id})
        ue.delete()
        UltimoEmbarazo.order_by_date(self.paciente)
        messages.success(self.request, u'Embarazo borrado')
        return reverse('partos:embarazos_ultimos_embarazos', kwargs={'paciente_id': self.paciente.id})


class PartogramaView(EstablecimientoRequiredMixin, CreateView):
    template_name = 'partos/partograma.html'
    model = PartogramaMedicion
    form_class = PartogramaMedicionForm
    # permissions = ('partos.change_partograma',)
    ingreso = None

    def get_form_custom(self, request, formcls, prefix):
        return formcls(request.POST or None, prefix=prefix)

    def get_context_data(self, **kwargs):
        context = super(PartogramaView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['fcfMs'] = ExamenFetalMedicionFormSet(self.request.POST)
            context['placentasM'] = PlacentaFormSet(self.request.POST)
        else:
            context['fcfMs'] = ExamenFetalMedicionFormSet()
            context['placentasM'] = PlacentaFormSet()
        try:
            referida = TerminacionEmbarazo.objects.get(ingreso=self._get_ingreso()).referido
            if referida:
                context.update({
                    'referida': referida})
        except:
            pass
        context.update({
            'ingreso': self._get_ingreso(),
            'partograma': self._get_partograma(),
            'terminacionembarazo_form': self.get_form_custom(self.request, TerminacionEmbarazoForm, 'atem_modal'),
            'lista_frecuencias': self._get_fcfs()
        })
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        if request.POST.get('atem_modal-hidden_name_form', '') == 'terminacion':
            aform = self.get_form_custom(
                request, TerminacionEmbarazoForm, 'atem_modal')
            if aform.is_valid():
                terminacion_embarazo = aform.save(commit=False)
                terminacion_embarazo.establecimiento_id = self.request.session[
                    'establecimiento_id']
                terminacion_embarazo.ingreso = self._get_ingreso()
                terminacion_embarazo.paciente = self._get_ingreso().paciente
                terminacion_embarazo.creator = self.request.user
                terminacion_embarazo.modifier = self.request.user
                try:
                    placentasM = PlacentaFormSet(self.request.POST)
                    with transaction.atomic():
                        self.object = aform.save()
                        if placentasM.is_valid():
                            placentasM.instance = self.object
                            placentasM.terminacion_embarazo = terminacion_embarazo
                            placentasM.save()
                    terminacion_embarazo.ingreso.partograma.status = Partograma.CERRADO
                    terminacion_embarazo.ingreso.partograma.save()
                    terminacion_embarazo.ingreso.embarazo.activo = False
                    terminacion_embarazo.ingreso.embarazo.save()
                    terminacion_embarazo.save()
                    messages.success(
                        request, 'Se cerro el partograma con exito.')
                    return HttpResponseRedirect(reverse('partos:home'))
                except IntegrityError as e:
                    messages.success(request, e.message)
                    return self.render_to_response(
                        {'ingreso': self._get_ingreso(), 'partograma': self._get_partograma(),
                         'terminacionembarazo_form': aform})
        else:
            form = self.form_class(request.POST)
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

    def get_form(self, form_class):

        form = super(PartogramaView, self).get_form(form_class)
        form.fields['fecha'].initial = datetime.today().date()
        last_medicion = self._get_partograma().mediciones.last()
        if last_medicion:
            form.fields[
                'tv_variedad_presentacion_val1'].initial = last_medicion.tv_variedad_presentacion_val1
            form.fields[
                'tv_variedad_presentacion_val2'].initial = last_medicion.tv_variedad_presentacion_val2
            if last_medicion and last_medicion.tv_membranas == 'rotas':
                form.fields[
                    'tv_membranas'].initial = last_medicion.tv_membranas
                form.fields[
                    'tv_membranas_rotas_tipo'].initial = last_medicion.tv_membranas_rotas_tipo
        return form

    def form_valid(self, form):
        medicion = form.save(commit=False)
        medicion.created_by = self.request.user
        medicion.partograma = self._get_partograma()
        last_medicion = self._get_partograma().mediciones.last()
        context = self.get_context_data()
        fcfMs = context['fcfMs']
        with transaction.atomic():
            self.object = form.save()
            if fcfMs.is_valid():
                fcfMs.instance = self.object
                fcfMs.medicion_parto = medicion
                fcfMs.save()
        if last_medicion and last_medicion.tv_membranas == 'rotas' and medicion.tv_membranas != 'rotas':
            form.errors['tv_membranas'] = [
                'Las membranas ya se encuentran rotas, esta intentando guardar un valor distinto']
            return self.form_invalid(form)
        return super(PartogramaView, self).form_valid(form)

    def get_success_url(self):
        return reverse('partos:partograma', kwargs={'ingreso_id': self._get_ingreso().id})

    def _get_ingreso(self):
        if self.ingreso is None:
            self.ingreso = get_object_or_404(
                Ingreso, id=self.kwargs.get('ingreso_id'))
        return self.ingreso

    def _get_partograma(self):

        ingreso = self._get_ingreso()
        values = {
            'establecimiento_id': self.request.session['establecimiento_id'],
            'paciente': ingreso.paciente,
            'ingreso': ingreso
        }

        try:
            partograma = Partograma.objects.get(ingreso=ingreso)
        except Partograma.DoesNotExist:
            partograma = Partograma(**values)
            partograma.created_by = self.request.user
            partograma.save()
        return partograma

    def _get_fcfs(self):
        mediciones = self._get_partograma().mediciones.all()
        lista_frecuencias = []
        for medicion in mediciones:
            frecuencias = ExamenFisicoFetal.objects.filter(
                medicion_parto=medicion).values()
            lista_frecuencias.append(frecuencias)
        return lista_frecuencias


class PartogramaMedicionUpdateView(EstablecimientoRequiredMixin, UpdateView):
    template_name = 'partos/partograma.html'
    model = PartogramaMedicion
    pk_url_kwarg = 'medicion_id'
    context_object_name = 'medicion'
    form_class = PartogramaMedicionForm
    ingreso = None

    def get_context_data(self, **kwargs):
        context = super(
            PartogramaMedicionUpdateView, self).get_context_data(**kwargs)
        context['fcfMs'] = ExamenFetalMedicionFormSet(
            queryset=ExamenFisicoFetal.objects.filter(medicion_parto=self.object.id), instance=self.object)
        try:
            referida = TerminacionEmbarazo.objects.get(ingreso=self._get_ingreso()).referido
            if referida:
                context.update({'referida': referida})
        except:
            pass
        context.update({
            'ingreso': self._get_ingreso(),
            'partograma': self._get_partograma(),
            'update_medicion': True
        })
        return context

    def get_success_url(self):
        return reverse('partos:partograma', kwargs={'ingreso_id': self._get_ingreso().id})

    def _get_ingreso(self):
        if self.ingreso is None:
            self.ingreso = get_object_or_404(
                Ingreso, id=self.kwargs.get('ingreso_id'))
        return self.ingreso

    def _get_partograma(self):
        ingreso = self._get_ingreso()
        values = {
            'establecimiento_id': self.request.session['establecimiento_id'],
            'paciente': ingreso.paciente,
            'ingreso': ingreso
        }
        try:
            partograma = Partograma.objects.get(ingreso=ingreso)
        except Partograma.DoesNotExist:
            partograma = Partograma(**values)
            partograma.created_by = self.request.user
            partograma.save()
        return partograma

    def form_valid(self, form):
        fcfMs = ExamenFetalMedicionFormSet(self.request.POST, instance=self.object)
        if fcfMs.is_valid():
            fcfMs.save()
        return super(PartogramaMedicionUpdateView, self).form_valid(form)


class PartogramaChartDataView(View):

    def get(self, request, *args, **kwargs):
        data = self._get_partograma().get_mediciones_dict()
        return JsonResponse(data)

    def _get_partograma(self):
        try:
            return Partograma.objects.get(ingreso_id=self.kwargs.get('ingreso_id', None))
        except Partograma.DoesNotExist:
            raise Http404


class PEcografiasView(EcografiasView):
    template_name = 'partos/ecografias.html'
    ingreso = None

    def get_context_data(self, **kwargs):
        context = super(PEcografiasView, self).get_context_data(**kwargs)
        context.update({
            'ingreso': self._get_ingreso(),
        })
        return context

    def _get_ingreso(self):
        if self.ingreso is None:
            self.ingreso = get_object_or_404(
                Embarazo, id=self.embarazo.id).ingreso
        return self.ingreso


class PEcografiaCreateView(EcografiaCreateView):
    template_name = 'partos/ecografia.html'
    ingreso = None

    def get_context_data(self, **kwargs):
        context = super(PEcografiaCreateView, self).get_context_data(**kwargs)
        context.update({
            'ingreso': self._get_ingreso(),
        })
        return context

    def _get_ingreso(self):
        if self.ingreso is None:
            self.ingreso = get_object_or_404(
                Embarazo, id=self.embarazo.id).ingreso
        return self.ingreso

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        Ecografia.order_by_date(self.embarazo)
        return reverse('partos:ecografias', kwargs={'paciente_id': self.paciente.id})


class PEcografiaUpdateView(EcografiaUpdateView):
    template_name = 'partos/ecografia.html'
    ingreso = None

    def get_context_data(self, **kwargs):
        context = super(PEcografiaUpdateView, self).get_context_data(**kwargs)
        context.update({
            'ingreso': self._get_ingreso(),
        })
        return context

    def _get_ingreso(self):
        if self.ingreso is None:
            self.ingreso = get_object_or_404(
                Embarazo, id=self.embarazo.id).ingreso
        return self.ingreso


class PEcografiaDeleteView(EcografiaDeleteView):

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        if self.object.created.date() < datetime.today().date():
            messages.warning(self.request, 'No puede eliminar ecografía anterior')
            return HttpResponseRedirect(reverse(
                'partos:ecografias', kwargs={'paciente_id': self.kwargs.get('paciente_id')}))
        return self.post(*args, **kwargs)

    def get_success_url(self):
        return reverse('partos:ecografias', kwargs={'paciente_id': self.kwargs.get('paciente_id')})


class PLaboratorioView(EstablecimientoRequiredMixin, UpdateView):
    template_name = 'partos/laboratorio.html'
    model = Laboratorio
    form_class = LaboratorioForm
    context_object_name = 'laboratorio'
    paciente = None  # referencias a las llaves
    embarazo = None  # referencias a las llaves
    ingreso = None

    def dispatch(self, request, *args, **kwargs):
        self.ingreso = self.get_ingreso(**kwargs)
        self.paciente = self.ingreso.paciente
        self.embarazo = self.ingreso.embarazo
        return super(PLaboratorioView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not hasattr(self, 'object'):
            try:
                self.object = self.model.objects.get(
                    paciente=self.paciente, embarazo=self.embarazo)
            except Laboratorio.DoesNotExist:

                last_control = self.ingreso.embarazo.controles.last()
                try:
                    if last_control:
                        self.object = self.model.objects.get(
                            control=last_control)
                        self.object.control = None
                        self.object.paciente = self.paciente
                        self.object.embarazo = self.embarazo
                        self.object.save()
                    else:
                        self.object = self.model.objects.create(
                            paciente=self.paciente, embarazo=self.embarazo, created_by=self.request.user)
                except Laboratorio.DoesNotExist:
                    self.object = self.model.objects.create(
                        paciente=self.paciente, embarazo=self.embarazo, created_by=self.request.user)
        return self.object

    def get_context_data(self, **kwargs):
        context = super(PLaboratorioView, self).get_context_data(**kwargs)
        context.update({
            'paciente': self.paciente,
            'embarazo': self.embarazo,
            'ingreso': self.ingreso
        })
        return context

    def get_ingreso(self, **kwargs):
        try:
            ingreso = Ingreso.objects.get(id=kwargs.get('ingreso_id', 0))
            return ingreso
        except Control.DoesNotExist:
            raise Http404

    def get_success_url(self):
        messages.success(self.request, u'Laboratorio actualizado')
        return reverse('partos:partograma', kwargs={'ingreso_id': self.ingreso.id})


class PSintomasView(EstablecimientoRequiredMixin, DetailView):
    model = Ingreso
    template_name = 'partos/sintomas.html'
    context_object_name = 'ingreso'
    pk_url_kwarg = 'ingreso_id'


    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        ingreso = self.get_object()
        if not ingreso.visito_sintomas:
            ingreso.visito_sintomas = True
            ingreso.save()
        return super(PSintomasView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        ingreso = self.get_object()
        ingreso.asintomatica = data['asintomatica']
        ingreso.save()
        if data['asintomatica']:
            ingreso.sintomas_ingreso.all().delete()
        else:
            for item in data['sintomas']:
                cie = ICD10.objects.get(codigo=item['codigo'])
                try:
                    sintoma = Sintoma.objects.get(cie=cie, ingreso=ingreso)
                except Sintoma.DoesNotExist:
                    sintoma = Sintoma.objects.create(
                        cie=cie, ingreso=ingreso, control=None, created_by=request.user)
                if item['delete']:
                    sintoma.delete()
                else:
                    sintoma.observacion = item['observacion']
                    sintoma.save()
            messages.success(request, u'Sintomas guardados')
        return JsonResponse({
            'url': reverse('partos:sintomas', kwargs={'ingreso_id': ingreso.id})
        })

    def get_context_data(self, **kwargs):
        context = super(PSintomasView, self).get_context_data(**kwargs)
        sintomas = Sintoma.objects.filter(ingreso=self.object)
        cies = self.get_cies()
        cies = cies.exclude(id__in=[sintoma.cie.id for sintoma in sintomas])
        context.update({
            'paciente': self.object.paciente,
            'cies': cies.order_by('nombre_mostrar', 'nombre'),
            'sintomas': sintomas,
            'asintomatica': self.object.asintomatica
        })
        return context

    def get_cies(self):
        codes = [
            'H109', 'H579', 'H931', 'I789', 'I951', 'N939', 'O121',
            'O208', 'O219', 'O363', 'O419', 'O624', 'R101', 'R103',
            'R104', 'R17X', 'R21X', 'R31X', 'R398', 'R418', 'R509',
            'R51X', 'R53X', 'R568', 'R601']
        return ICD10.objects.filter(codigo__in=codes)


class HojaMonitoreoMaternoFetalReportView(View):

    def get(self, request, *args, **kwargs):
        control = get_object_or_404(
            Partograma, id=kwargs.get('partograma_id', ''))
        report = reports.HojaMonitoreoMaternoFetalReport(control)
        return report.render_to_response()


class PartosControlesPrenatalReportView(View):

    def get(self, request, *args, **kwargs):
        embarazo = get_object_or_404(
            Embarazo, id=kwargs.get('embarazo_id', ''))
        report = reports.PartosControlesPrenatalReport(embarazo)
        return report.render_to_inlineresponse()


class PartosHistoriaClinicaReportView(View):

    def get(self, request, *args, **kwargs):
        embarazo = get_object_or_404(
            Embarazo, id=kwargs.get('embarazo_id', ''))
        report = reports.PartosHistoriaClinicaReport(embarazo)
        return report.render_to_response()


Point = namedtuple('Point', ['x', 'y'])


class CanvasCommonMethodsMixin(object):
    c = None

    def draw_x(self, _x, _y, size=1):
        self.c.line(_x - size, _y - size, _x + size, _y + size)
        self.c.line(_x + size, _y - size, _x - size, _y + size)

    def draw_arrow(self, x1, y1, x2, y2, d=12):
        """
        Down to up
        """
        self.c.line(x1 - d / 2, y1, x1 + d / 2, y1)
        self.c.line(x2 - d / 2, y2, x2 + d / 2, y2)

        w = d / 6
        h = d / 3

        line_width = self.c._lineWidth

        path_down = self.c.beginPath()
        path_down.moveTo(x1, y1 + line_width / 2)
        path_down.lineTo(x1 - w, y1 + h)
        path_down.lineTo(x1, y1 + h - h / 4)
        path_down.lineTo(x1 + w, y1 + h)
        path_down.lineTo(x1, y1 + line_width / 2)
        self.c.drawPath(path_down, stroke=0, fill=1)

        path_up = self.c.beginPath()
        path_up.moveTo(x2, y2 - line_width / 2)
        path_up.lineTo(x2 - w, y2 - h)
        path_up.lineTo(x2, y2 - h + h / 4)
        path_up.lineTo(x2 + w, y2 - h)
        path_up.lineTo(x2, y2 - line_width / 2)
        self.c.drawPath(path_up, stroke=0, fill=1)

        self.c.line(x1, y1 + h / 2, x2, y2 - h / 2)


class PartogramaReportView(CanvasCommonMethodsMixin, PdfView):
    filename = 'partograma_{}.pdf'
    partograma = None
    paciente = None
    usuario = None
    c = None
    data = None

    def dispatch(self, request, *args, **kwargs):
        self.partograma = get_object_or_404(Partograma, id=kwargs.get('partograma_id'))
        self.usuario = get_object_or_404(User, dni=self.partograma.created_by)
        self.paciente = self.partograma.paciente
        self.filename = self.filename.format(self.paciente.numero_documento)
        self.data = self.partograma.get_mediciones_dict()
        self.ingreso = get_object_or_404(Ingreso, id=self.partograma.ingreso_id)
        return super(PartogramaReportView, self).dispatch(request, *args, **kwargs)

    def process_canvas(self, c):
        self.c = c
        self._calculate_base_x()
        self.header()
        self.block1()
        self.block2()
        self.c.setLineWidth(0.5)
        self.block3()
        self.block4()
        c.setFontSize(5)
        for val in range(11):
            c.drawString(210, 520 + val * 7, str(val).rjust(3, b' '))
        for val in range(1, 6):
            c.drawString(210, 445 + val * 7, str(val).rjust(3, b' '))
        values = tuple(range(60, 180, 10))
        for val in range(12):
            c.drawString(205, 270 + val * 7, str(values[val]).rjust(3, b' '))
        c.drawString(188, 515, 'Nº HORAS')
        c.drawString(195, 508, 'HORAS')
        c.showPage()
        return c

    def _calculate_base_x(self):
        self.base_x = 230
        try:
            dilatacion = int(self.data[1]['dilatacion'])
            if dilatacion >= 4:
                self.base_x += (dilatacion - 4) * 24
        except ValueError:
            pass

    def grid(self, x=0, y=0, rows=1, cols=1, w=10, h=10):
        for i in range(cols):
            for j in range(rows):
                path = self.c.beginPath()
                _x = i * w + x
                _y = j * h + y
                path.moveTo(_x, _y)
                path.lineTo(_x, _y + h)
                path.lineTo(_x + w, _y + h)
                path.lineTo(_x + w, _y)
                path.lineTo(_x, _y)
                self.c.drawPath(path)

    def draw_rect_stripped(self, x, y, w, h, sep=1):
        self.c.rect(x, y, w, h)
        p1 = []
        p2 = []
        for i in range(y + h, y, -sep):
            p1.append(Point(x=x, y=i))
        for i in range(x, x + w, sep):
            p1.append(Point(x=i, y=y))
            p2.append(Point(x=i, y=y + h))
        for i in range(y + h, y, -sep):
            p2.append(Point(x=x + w, y=i))
        for i in range(len(p1)):
            self.c.line(p1[i].x, p1[i].y, p2[i].x, p2[i].y)

    def draw_rect_circle(self, x, y, w, h, sep=1):
        self.c.rect(x, y, w, h)
        r = 1
        for i in range(x + r + r / 2, x + w, r * 2 + 1):
            for j in range(y + r + r / 2, y + h, r * 2 + 1):
                self.c.circle(i + r / 2.0, j + r / 2.0, r, stroke=0, fill=1)

    def draw_diagonal_text(self, x, y, angle, size, text):
        self.c.saveState()
        self.c.translate(x, y)
        self.c.rotate(angle)
        self.c.setFontSize(size)
        self.c.setFillColor('gray')
        self.c.drawString(0, 0, text)
        self.c.restoreState()

    def header(self):
        self.c.drawImage('static/img/logo_minsa.png', 15, 785, 127, 50)
        self.c.setFontSize(15)
        self.c.drawCentredString(298, 800, 'PARTOGRAMA DE LA OMS MODIFICADO')
        self.c.setFontSize(7)
        self.c.setFontSize(6)
        self.c.drawString(30, 780, 'NOMBRE: ')
        self.c.setFontSize(6)
        self.c.drawString(70, 780, '{}'.format(self.paciente.nombre_completo))
        self.c.setFontSize(7)
        self.c.drawString(300, 780, 'GRAVIDEZ: {}'.format(self.paciente.ultimos_embarazos.count() + 1))
        self.c.drawString(360, 780, 'PARIDAD: {}'.format(
            self.paciente.antecedente_obstetrico.partos if hasattr(self.paciente, 'antecedente_obstetrico') else 0))
        historia = self.paciente.historias_clinicas.all().order_by('-modified').first()
        self.c.drawString(420, 780, 'Nº HISTORIA CLÍNICA: {}'.format(historia.numero))
        self.c.drawString(30, 765, 'FECHA DE INGRESO: {}'.format(self.partograma.ingreso.fecha.strftime('%d/%m/%Y')))
        self.c.drawString(200, 765, 'HORA DE INGRESO: {}'.format(self.partograma.ingreso.hora.strftime('%H:%M')))
        medicion_membrana_rota = self.partograma.mediciones.filter(tv_membranas='rotas').order_by('hora').first()
        hora = ''
        minutos = ''
        if self.ingreso.tiempo_ruptura_membranas_horas:
            hora = '{} H'.format(self.ingreso.tiempo_ruptura_membranas_horas)
        if self.ingreso.tiempo_ruptura_membranas_minutos:
            minutos = '{} min'.format(self.ingreso.tiempo_ruptura_membranas_minutos)
        self.c.drawString(350, 765, 'TIEMPO DE MEMBRANAS ROTAS: {} {}'.format(hora, minutos))

    def block1(self):
        self.c.setLineWidth(0.5)
        self.grid(x=220, y=640, rows=13, cols=24, w=12, h=7)
        self.grid(x=220, y=620, rows=2, cols=24, w=12, h=7)

        self.c.setFontSize(7)
        self.c.drawString(20, 700, 'FCF')
        self.c.drawString(20, 670, 'INTEGRAS: I')
        self.c.drawString(20, 660, 'ROTAS: R')
        self.c.drawString(20, 650, 'LIQ. CLARO: C')
        self.c.drawString(20, 640, 'LIQ. MECONIAL: M')
        self.c.drawString(20, 630, 'LIQ. SANGUINOLENTO: S')
        self.c.setFontSize(6)
        self.c.drawString(150, 630, 'Líquido amniótico')
        self.c.drawString(150, 620, 'Moldeaminetos')
        self.c.setFontSize(5)
        values = tuple(range(80, 210, 10))
        for val in range(13):
            self.c.drawString(
                205, 639.5 + val * 7, str(values[val]).rjust(3, b' '))

        self.c.setFontSize(6)
        moldeaminetos_base = Point(self.base_x - 5, 622)
        liquido_amniotico_base = Point(self.base_x - 5, 629)
        fcf_init = Point(self.base_x - 10, 640)

        puntos = []
        contador = 0
        for index in range(24):
            self.c.drawString(
                moldeaminetos_base.x + 12 * index, moldeaminetos_base.y,
                              self.data[index + 1]['moldeaminetos'] or '')
            self.c.drawString(
                liquido_amniotico_base.x + 12 *
                    index, liquido_amniotico_base.y,
                              self.data[index + 1]['liquido_amniotico'] or '')
            _fcf = self.data[index + 1]['fcf']

            if _fcf:
                _fcf_split = _fcf.split()
                if contador == 0:
                    puntos = [[] for i in range(len(_fcf_split))]
                    contador += 1
                for i in range(0, len(_fcf_split)):
                    puntos[i].append(
                        (fcf_init.x + 12 * index, fcf_init.y + ((int(_fcf_split[i]) - 80) / 10.0) * 7))

        if puntos:
            self.c.setLineWidth(1.5)
            for elemento in puntos:
                path = self.c.beginPath()
                path.moveTo(elemento[0][0], elemento[0][1])
                for _x, _y in elemento[1:]:
                    path.lineTo(_x, _y)
                self.c.setStrokeColor('blue')
                self.c.drawPath(path)
                self.c.setStrokeColor('black')

    def block2(self):
        self.c.setLineWidth(0.5)
        self.grid(x=220, y=520, rows=10, cols=24, w=12, h=7)
        self.grid(x=220, y=506, rows=2, cols=12, w=24, h=7)

        self.draw_diagonal_text(255, 562, 18, 12, 'ALERTA')
        self.draw_diagonal_text(390, 556, 16, 12, 'ACCIÓN')

        self.c.setLineWidth(1)

        self.c.line(220, 548, 364, 590)
        self.c.line(316, 548, 460, 590)

        self.c.line(40, 590, 60, 590)
        self.c.line(50, 520, 50, 550)
        self.c.line(50, 565, 50, 590)
        self.c.line(40, 520, 60, 520)
        self.c.setFontSize(4)
        self.c.drawCentredString(50, 560, 'CUELLO UTERINO (CM)')
        self.c.drawCentredString(50, 553, 'TRAZO X')

        self.c.line(120, 570, 140, 570)
        self.c.line(130, 520, 130, 535)
        self.c.line(130, 550, 130, 570)
        self.c.line(120, 520, 140, 520)

        self.c.drawCentredString(130, 545, 'DESCENSO CEFALICO')
        self.c.drawCentredString(130, 538, '(TRAZO O)')

        dilatacion_points = []
        descenso_cefalico_points = []

        init = Point(self.base_x - 10, 520)

        # Print hours

        self.c.saveState()
        self.c.setFontSize(6)
        for i in range(0, 12):
            self.c.drawString(230 + i * 24, 514, str(i + 1))
        for i in range(0, 12):
            if self.base_x + i * 24 > 320 + 8 * 24:
                continue
            hora_key = i * 2 + 1
            self.c.drawString(
                self.base_x + i * 24 - 6, 508, self.data[hora_key].get('hora', ''))

        self.c.restoreState()

        for index in range(24):
            dilatacion = self.data[index + 1]['dilatacion']
            descenso_cefalico = self.data[index + 1]['descenso_cefalico']
            if dilatacion and isinstance(dilatacion, int):
                dilatacion = int(dilatacion)
                dilatacion_points.append((init.x + 12 * index, init.y + dilatacion * 7))
            if isinstance(descenso_cefalico, int) and descenso_cefalico >= 0:
                descenso_cefalico = int(descenso_cefalico)
                descenso_cefalico_points.append((init.x + 12 * index, init.y + descenso_cefalico * 7))

        if dilatacion_points:
            self.c.setLineWidth(1.5)
            path = self.c.beginPath()
            path.moveTo(dilatacion_points[0][0], dilatacion_points[0][1])
            self.draw_x(dilatacion_points[0][
                        0], dilatacion_points[0][1], size=2)
            for _x, _y in dilatacion_points[1:]:
                path.lineTo(_x, _y)
                self.draw_x(_x, _y, size=2)
            self.c.setStrokeColor('red')
            self.c.drawPath(path)
            self.c.setStrokeColor('black')

        if descenso_cefalico_points:
            self.c.setLineWidth(1.5)
            path = self.c.beginPath()
            path.moveTo(descenso_cefalico_points[
                        0][0], descenso_cefalico_points[0][1])
            self.c.setFillColorRGB(0, 0, 0)
            self.c.circle(descenso_cefalico_points[0][
                          0], descenso_cefalico_points[0][1], 2, stroke=0, fill=1)
            for _x, _y in descenso_cefalico_points[1:]:
                path.lineTo(_x, _y)
                self.c.setFillColorRGB(0, 0, 0)
                self.c.circle(_x, _y, 2, stroke=0, fill=1)
            self.c.setStrokeColor('blue')
            self.c.drawPath(path)
            self.c.setStrokeColor('black')

    def block3(self):
        self.grid(x=220, y=450, rows=5, cols=24, w=12, h=7)

        self.grid(x=220, y=420, rows=2, cols=24, w=12, h=7)
        self.c.setFontSize(5)
        self.c.drawString(50, 475, 'MENOR DE 20')
        self.draw_rect_circle(90, 473, 12, 7)
        self.c.drawString(50, 465, 'ENTRE 20 Y 40')
        self.draw_rect_stripped(90, 463, 12, 7, sep=4)
        self.c.drawString(50, 455, 'MAYOR DE 40')
        self.c.rect(90, 453, 12, 7, stroke=1, fill=1)

        self.c.setFontSize(5)
        self.c.drawString(180, 429, 'OXITOCINA UL')
        self.c.drawString(180, 422, 'GOTAS / MIN.')
        init = Point(x=self.base_x - 8, y=422)
        self.c.setFillColorRGB(0, 0, 0)
        for index in range(24):
            goteo = self.data[index + 1]['goteo']
            oxitocina = self.data[index + 1]['oxitocina']
            duracion = self.data[index + 1]['duracion']
            frecuencia = self.data[index + 1]['frecuencia']
            if oxitocina:
                self.c.drawString(init.x + 12 * index, init.y + 7, oxitocina)
            if goteo:
                self.c.drawString(init.x + 12 * index, init.y, goteo)

            if frecuencia in ('1/10', '2/10', '3/10', '4/10', '5+/10') and duracion:
                frecuencia = int(frecuencia[0])
                if duracion == '40+':
                    self.c.rect(
                        init.x - 2 + 12 * index, init.y + 28, 12, 7 * frecuencia, stroke=0, fill=1)
                elif duracion == '-20':
                    self.draw_rect_circle(
                        init.x - 2 + 12 * index, init.y + 28, 12, 7 * frecuencia, sep=4)
                else:
                    self.draw_rect_stripped(
                        init.x - 2 + 12 * index, init.y + 28, 12, 7 * frecuencia, sep=4)

    def block4(self):
        self.c.setLineWidth(0.5)
        self.grid(x=220, y=270, rows=17, cols=24, w=12, h=7)

        self.grid(x=220, y=240, rows=1, cols=24, w=12, h=7)

        self.grid(x=220, y=210, rows=3, cols=24, w=12, h=7)

        self.c.drawCentredString(60, 370, 'PULSO')
        self.c.circle(60, 365, 2, stroke=1, fill=1)
        self.c.drawCentredString(50, 333, 'PRESION')
        self.c.drawCentredString(50, 323, 'ARTERIAL')
        self.draw_arrow(75, 310, 75, 345)

        self.c.drawString(70, 240, 'TEMPERATURA')

        self.c.drawString(70, 220, 'ORINA')
        path = self.c.beginPath()
        path.moveTo(105, 231)
        path.lineTo(103, 229)
        path.lineTo(103, 223)
        path.lineTo(101, 221)
        path.lineTo(103, 219)
        path.lineTo(103, 213)
        path.lineTo(105, 211)
        self.c.drawPath(path)
        self.c.drawString(110, 227, 'PROTEINA')
        self.c.drawString(110, 220, 'ACETONA')
        self.c.drawString(110, 213, 'VOLUMEN')

        self.c.setFontSize(10)
        self.c.drawString(70, 150, 'RESPONSABLE DE LA ATENCIÓN: {}'.format(self.usuario.get_full_name()))

        pulso_points = []
        init = Point(x=self.base_x - 10, y=270)

        temp_init = Point(x=self.base_x - 9, y=242)
        orin_init = Point(x=self.base_x - 9, y=212)
        self.c.setFontSize(5)
        self.c.setLineWidth(1.5)
        for index in range(24):
            self.c.drawString(temp_init.x + 12 * index, temp_init.y, str(
                self.data[index + 1]['temperatura']) or '')
            self.c.drawString(orin_init.x + 12 * index, orin_init.y + 12.5, str(
                self.data[index + 1]['orina_proteinas']) or '')
            self.c.drawString(orin_init.x + 12 * index, orin_init.y + 6.5, str(
                self.data[index + 1]['orina_cetona']) or '')
            self.c.drawString(orin_init.x + 12 * index, orin_init.y, str(
                self.data[index + 1]['orina_volumen']) if self.data[index + 1]['orina_volumen'] is not None else '')
            pulso = self.data[index + 1]['pulso']
            sistolica = self.data[index + 1]['sistolica']
            diastolica = self.data[index + 1]['diastolica']
            if pulso:
                pulso_points.append(
                    Point(x=init.x + 12 * index, y=init.y + ((pulso - 60) / 10.0) * 7))
            if sistolica and diastolica:
                self.draw_arrow(init.x + 12 * index + 6, init.y + ((diastolica - 60) / 10.0) * 7,
                                init.x + 12 * index + 6, init.y + ((sistolica - 60) / 10.0) * 7)

        if pulso_points:
            path = self.c.beginPath()
            first_point = pulso_points[0]
            path.moveTo(first_point.x, first_point.y)
            self.c.circle(first_point.x, first_point.y, 2, stroke=0, fill=1)
            for _x, _y in pulso_points[1:]:
                path.lineTo(_x, _y)
                self.c.circle(_x, _y, 2, stroke=0, fill=1)
            self.c.setStrokeColor('red')
            self.c.drawPath(path)
            self.c.setStrokeColor('black')


class GraficaControlesVitalesView(CanvasCommonMethodsMixin, PdfView):
    filename = 'graficas_controles_vitales_{}.pdf'
    partograma = None
    paciente = None
    establecimiento = None
    _data = {}

    def dispatch(self, request, *args, **kwargs):
        self.partograma = get_object_or_404(
            Partograma, id=kwargs.get('partograma_id'))
        self.paciente = self.partograma.paciente
        self.filename = self.filename.format(self.paciente.numero_documento)
        self.establecimiento = self.partograma.establecimiento
        return super(GraficaControlesVitalesView, self).dispatch(request, *args, **kwargs)

    def process_canvas(self, c):
        self.c = c
        self._data = self._prepare_data()
        self._header()
        self._table_header()
        self._table_body()
        self._table_footer()
        self._make_legend()
        return c

    def _header(self):
        _y = 760
        self.c.saveState()
        self.c.setFontSize(5)
        self.c.drawCentredString(80, _y + 60, 'GOBIERNO REGIONAL DEL CALLAO')
        self.c.drawCentredString(80, _y + 50, 'GERENCIA REGIONAL DEL CALLAO')
        self.c.drawCentredString(
            80, _y + 40, self.establecimiento.diresa.nombre.upper())
        self.c.drawCentredString(
            80, _y + 30, self.establecimiento.red.nombre.upper())
        self.c.drawCentredString(
            80, _y + 20, self.establecimiento.microred.nombre.upper())
        self.c.drawCentredString(
            80, _y + 10, self.establecimiento.nombre.upper())
        self.c.setFontSize(16)
        self.c.drawCentredString(
            self.c._pagesize[0] / 2.0, _y, 'GRÁFICAS DE CONTROLES VITALES')
        self.c.restoreState()

    def _table_header(self):
        _x, _y = 30, 710
        w, h = 10, 10
        self.c.saveState()
        self.c.setFontSize(8)
        # PA
        self.c.rect(_x, _y, 4 * w, h)
        self.c.drawCentredString((2 * _x + 4 * w) / 2.0, _y + 3, 'PA')
        # PULSO
        self.c.rect(_x + w * 4, _y, 4 * w, h)
        self.c.drawCentredString((2 * _x + 12 * w) / 2.0, _y + 3, 'PULSO')
        # TEMP
        self.c.rect(_x + 2 * w * 4, _y, w * 4, h)
        self.c.drawCentredString((2 * _x + 20 * w) / 2.0, _y + 3, 'TEMP')
        # DIAS DE HOSPITALIZACION
        self.c.rect(_x, _y + h, 12 * w, h)
        self.c.drawCentredString(
            (2 * _x + 12 * w) / 2.0, _y + h + 3, 'DIAS DE HOSPITALIZACION')
        # FECHA
        self.c.rect(_x, _y + 2 * h, 12 * w, h)
        self.c.drawCentredString(
            (2 * _x + 12 * w) / 2.0, _y + 2 * h + 3, 'FECHA')

        for i in range(0, 39, 3):
            self.c.rect(_x + 12 * w + i * w, _y + h, w * 3, h)
            self.c.rect(_x + 12 * w + i * w, _y + 2 * h, w * 3, h)

        self.c.saveState()
        self.c.setFontSize(5)
        for key, value in self._data.iteritems():
            self.c.drawCentredString(_x + (w / 2.0) + 10 * w + (
                3 * w * key), _y + 2 * h + 3, value['fecha'])
        # MTN
        self.c.restoreState()
        flag = 0
        for i in range(39):
            new_x = _x + 12 * w
            flag = flag + 1 if flag != 3 else 1
            if flag == 1:
                self.c.rect(new_x + i * w, _y, w * 2, h)
                self.c.drawCentredString(
                    (2 * new_x + 2 * i * w + w) / 2.0, _y + 2, 'M')
            elif flag == 2:
                self.c.rect(new_x + i * w, _y, w, h)
                self.c.drawCentredString(
                    (2 * new_x + 2 * i * w + w) / 2.0, _y + 2, 'T')
            elif flag == 3:
                self.c.rect(new_x + i * w, _y, w, h)
                self.c.drawCentredString(
                    (2 * new_x + 2 * i * w + w) / 2.0, _y + 2, 'N')
        self.c.restoreState()

    def _table_body(self):
        _x, _y = 30, 278

        w, h = 10, 8
        d_x, d_y = _x + w * 12, _y
        for i in range(0, 12, 4):
            self.c.rect(_x + i * w, _y, w * 4, 54 * h)

        pa_values = ('10', '20', '30', '40', '50', '60',
                     'RESP', '0', '50', '100', '150', '200', '250')
        pulso_values = ('40', '50', '60', '70', '80', '90',
                        '100', '110', '120', '130', '140', '150', '160')
        temp_values = ('35', '36', '37', '38', '39', '40', '41')
        self.c.setFontSize(10)
        sep = 34
        for i in range(len(pa_values)):
            self.c.drawCentredString(
                (2 * _x + 4 * w) / 2.0, _y + i * sep + 3, pa_values[i])
            self.c.drawCentredString(
                (2 * _x + 12 * w) / 2.0, _y + i * sep + 3, pulso_values[i])

        for i in range(len(temp_values)):
            self.c.drawCentredString(
                (2 * _x + 20 * w) / 2.0, _y + 173 + i * sep, temp_values[i])

        for i in range(0, 39):
            for j in range(54):
                self.c.rect(_x + 12 * w + i * w, _y + j * h, w, h)

        half_square = w / 2.0
        for key, value in self._data.iteritems():
            day_x = d_x + (key - 1) * 3 * w
            for a in ('m', 't', 'n'):
                if a == 'm':
                    __x = day_x + half_square
                elif a == 't':
                    __x = day_x + w + half_square
                else:
                    __x = day_x + w * 2 + half_square
                v = value[a]
                if 'pulso' in v and v['pulso']:
                    __y = d_y + \
                        ((v['pulso'] - 40) * sep / 10) + 3 + half_square
                    self.c.circle(__x, __y, 3, fill=1)
                if 'frecuencia_respiratoria' in v and v['frecuencia_respiratoria']:
                    __y = d_y + \
                        ((v['frecuencia_respiratoria'] - 10) * sep / 10) + \
                         3 + half_square
                    self.c.circle(__x, __y, 3)
                if 'temperatura' in v and v['temperatura']:
                    __y = d_y + \
                        ((v['temperatura'] - 35) * sep) + half_square + 173
                    self.draw_x(__x, __y, 4)
                if 'presion_sistolica' in v and 'presion_diastolica' in v and v['presion_sistolica'] and v[
                        'presion_diastolica']:
                    _y1 = d_y + (v['presion_sistolica'] * sep / 50) + 3 + half_square + 7 * sep
                    _y2 = d_y + (v['presion_diastolica'] * sep / 50) + 3 + half_square + 7 * sep
                    self.draw_arrow(__x, _y2, __x, _y1, w)

    def _make_legend(self):
        _x, _y = 40, 35
        self.draw_x(_x, _y, 3)
        self.c.circle(_x, _y + 10, 3, fill=1)
        self.c.circle(_x, _y + 20, 3)
        self.draw_arrow(_x, _y + 30, _x, _y + 40, 10)
        self.c.drawString(_x + 10, _y - 3, 'Temperatura')
        self.c.drawString(_x + 10, _y + 7, 'Pulso')
        self.c.drawString(_x + 10, _y + 18, 'Frecuencia Respiratoria')
        self.c.drawString(_x + 10, _y + 32, 'Presión Arterial')

    def _table_footer(self):
        _x, _y = 30, 143
        w, h = 10, 15
        self.c.saveState()
        names = ('ORAL', 'PARENTERAL', 'ORINA', 'VOMITOS',
                 'HECES', 'PESO', 'TALLA', 'SONA URINARIA', 'MENSTRUACION')
        names = tuple(reversed(names))
        self.c.setFontSize(8)
        for i in range(len(names)):
            self.c.rect(_x, _y + i * h, w * 12, h)
            self.c.drawCentredString(
                (2 * _x + w * 12) / 2.0, _y + i * h + 3, names[i])
        for i in range(0, 39):
            for j in range(len(names)):
                self.c.rect(_x + 12 * w + i * w, _y + j * h, w, h)
        self.c.rect(_x, _y - h, 14 * w, h)
        self.c.drawCentredString(
            (2 * _x + 14 * w) / 2.0, _y - h + 3, 'APELLIDO PATERNO')
        self.c.rect(_x + 14 * w, _y - h, 14 * w, h)
        self.c.drawCentredString(
            (2 * _x + 42 * w) / 2.0, _y - h + 3, 'APELLIDO MATERNO')
        self.c.rect(_x + 28 * w, _y - h, 23 * w, h)
        self.c.drawCentredString(
            (2 * _x + 79 * w) / 2.0, _y - h + 3, 'NOMBRES')
        self.c.rect(_x, _y - 2 * h, 14 * w, h)
        self.c.drawCentredString(
            (2 * _x + 14 * w) / 2.0, _y - 2 * h + 3, self.paciente.apellido_paterno.upper())
        self.c.rect(_x + 14 * w, _y - 2 * h, 14 * w, h)
        self.c.drawCentredString(
            (2 * _x + 42 * w) / 2.0, _y - 2 * h + 3, self.paciente.apellido_materno.upper())
        self.c.rect(_x + 28 * w, _y - 2 * h, 23 * w, h)
        self.c.drawCentredString((2 * _x + 79 * w) / 2.0, _y - 2 * h + 3, self.paciente.nombres.upper())
        self.c.rect(_x, _y - 3 * h, 14 * w, h)
        self.c.drawCentredString(
            (2 * _x + 14 * w) / 2.0, _y - 3 * h + 3, 'SERVICIO')
        self.c.rect(_x + 14 * w, _y - 3 * h, 14 * w, h)
        self.c.drawCentredString(
            (2 * _x + 42 * w) / 2.0, _y - 3 * h + 3, 'Nº CAMA')
        self.c.rect(_x + 28 * w, _y - 3 * h, 23 * w, h)
        self.c.drawCentredString(
            (2 * _x + 79 * w) / 2.0, _y - 3 * h + 3, 'HISTORIA CLINICA')
        self.c.rect(_x, _y - 4 * h, 14 * w, h)
        self.c.drawCentredString((2 * _x + 14 * w) / 2.0, _y - 4 * h + 3, '')
        self.c.rect(_x + 14 * w, _y - 4 * h, 14 * w, h)
        self.c.drawCentredString((2 * _x + 42 * w) / 2.0, _y - 4 * h + 3, '')
        self.c.rect(_x + 28 * w, _y - 4 * h, 23 * w, h)
        hc = self.paciente.historias_clinicas.filter(
            establecimiento=self.establecimiento).first()
        self.c.drawCentredString(
            (2 * _x + 79 * w) / 2.0, _y - 4 * h + 3, str(hc.numero) if hc else '')
        self.c.restoreState()

    @staticmethod
    def _prepare_value(medicion):
        if medicion is None:
            return {

            }
        return {
            'presion_sistolica': medicion.presion_sistolica or '',
            'presion_diastolica': medicion.presion_diastolica or '',
            'temperatura': medicion.temperatura or '',
            'pulso': medicion.pulso or '',
            'frecuencia_respiratoria': medicion.frecuencia_respiratoria or ''
        }

    def _prepare_data(self):
        partograma_mediciones = self.partograma.mediciones.all().order_by(
            'fecha', 'hora')
        puerperio_mediciones = MonitoreoMedicion.objects.filter(
            monitoreo__terminacion_embarazo=self.partograma.ingreso.terminacion_embarazo).order_by('fecha', 'hora')

        first_medicion = partograma_mediciones.first()
        initial_date = first_medicion.fecha
        data = defaultdict(dict)
        m_time = time(hour=0, minute=0, second=0)
        t_time = time(hour=8, minute=0, second=0)
        n_time = time(hour=16, minute=0, second=0)
        end_time = time(hour=23, minute=59, second=59)
        counter = 1
        max_measurements = 14
        while counter < partograma_mediciones.count() and counter < max_measurements:
            m = partograma_mediciones.filter(fecha=initial_date, hora__range=[m_time, t_time]).first()
            t = partograma_mediciones.filter(fecha=initial_date, hora__range=[t_time, n_time]).first()
            n = partograma_mediciones.filter(fecha=initial_date, hora__range=[n_time, end_time]).first()
            data[counter] = {
                'fecha': initial_date.strftime('%d/%m/%Y'),
                'm': self._prepare_value(m),
                't': self._prepare_value(t),
                'n': self._prepare_value(n),
            }
            initial_date += timedelta(days=1)
            counter += 1
        while counter < max_measurements:
            m = puerperio_mediciones.filter(
                fecha=initial_date, hora__range=[m_time, t_time]).first()
            t = puerperio_mediciones.filter(
                fecha=initial_date, hora__range=[t_time, n_time]).first()
            n = puerperio_mediciones.filter(
                fecha=initial_date, hora__range=[n_time, end_time]).first()
            data[counter] = {
                'fecha': initial_date.strftime('%d/%m/%Y'),
                'm': self._prepare_value(m),
                't': self._prepare_value(t),
                'n': self._prepare_value(n),
            }
            initial_date += timedelta(days=1)
            counter += 1
        return data


class TerminacionEmbarazoCreateView(EstablecimientoRequiredMixin, CreateView):
    template_name = 'partos/terminacion_embarazo.html'
    model = TerminacionEmbarazo
    form_class = TerminacionEmbarazoForm
    ingreso = None

    def dispatch(self, request, *args, **kwargs):
        self.ingreso = get_object_or_404(Ingreso, id=kwargs.get('ingreso_id'))
        if not hasattr(self.ingreso, 'partograma'):
            return HttpResponseRedirect(reverse('partos:partograma', kwargs={'ingreso_id': self.ingreso.id}))
        if self.ingreso.partograma.status == Partograma.CERRADO:
            messages.warning(request,
                             'No se puede registrar la terminación de un embarazo a partir de un partograma cerrado')
            return HttpResponseRedirect(reverse('partos:partograma', kwargs={'ingreso_id': self.ingreso.id}))
        return super(TerminacionEmbarazoCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        terminacion_embarazo = form.save(commit=False)
        terminacion_embarazo.establecimiento_id = self.request.session[
            'establecimiento_id']
        terminacion_embarazo.ingreso = self.ingreso
        terminacion_embarazo.paciente = self.ingreso.paciente
        terminacion_embarazo.hora = datetime.now().time()
        terminacion_embarazo.creator = self.request.user
        terminacion_embarazo.modifier = self.request.user
        terminacion_embarazo.save()
        self.ingreso.partograma.status = Partograma.CERRADO
        self.ingreso.partograma.save()
        self.ingreso.embarazo.activo = False
        self.ingreso.embarazo.save()
        return super(TerminacionEmbarazoCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(
            TerminacionEmbarazoCreateView, self).get_context_data(**kwargs)
        context.update({
            'paciente': self.ingreso.paciente,
            'ingreso': self.ingreso
        })
        return context

    def get_success_url(self):
        messages.success(self.request, 'Terminación de embarazo registrada')
        return reverse('partos:home')


class TerminacionEmbarazoUpdateView(EstablecimientoRequiredMixin, UpdateView):
    template_name = 'partos/terminacion_embarazo.html'
    model = TerminacionEmbarazo
    form_class = TerminacionEmbarazoForm
    pk_url_kwarg = 'terminacion_embarazo_id'
    ingreso = None

    def get_context_data(self, **kwargs):
        context = super(
            TerminacionEmbarazoUpdateView, self).get_context_data(**kwargs)
        context.update({
            'paciente': self.object.paciente,
            'ingreso': self.object.ingreso
        })
        return context

    def get_success_url(self):
        messages.success(self.request, 'Terminación de embarazo actualizada')
        return reverse('partos:home')


class UltimoControlView(EstablecimientoRequiredMixin, UpdateView):
    template_name = 'partos/control_last.html'
    model = Control
    form_class = ControlForm
    pk_url_kwarg = 'id'
    context_object_name = 'control'

    def get_context_data(self, **kwargs):

        context = super(UltimoControlView, self).get_context_data(**kwargs)

        try:
            control = Control.objects.get(paciente=self.object.paciente.id, numero=1)
            primer_control_presion_diastolica = control.presion_diastolica
            primer_control_presion_sistolica = control.presion_sistolica
        except Exception as e:
            primer_control_presion_diastolica = -1
            primer_control_presion_sistolica = -1

        context.update({
            'paciente': self.object.paciente,
            'embarazo': self.object.embarazo,
            'primer_control_presion_diastolica': primer_control_presion_diastolica,
            'primer_control_presion_sistolica': primer_control_presion_sistolica
        })

        return context


class PExamenFisicoView(EstablecimientoRequiredMixin, UpdateView):
    template_name = 'partos/examen_fisico.html'
    model = ExamenFisico
    form_class = ExamenFisicoIngresoForm
    context_object_name = 'examen_fisico'
    ingreso = None

    # permissions = ('controles.change_examenfisico',)

    def dispatch(self, request, *args, **kwargs):
        self.ingreso = self.get_ingreso(**kwargs)
        return super(PExamenFisicoView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            obj = self.model.objects.get(ingreso=self.ingreso)
        except ExamenFisico.DoesNotExist:
            obj = self.model.objects.create(control=None, ingreso=self.ingreso, created_by=self.request.user)
        return obj

    def get_context_data(self, **kwargs):
        context = super(PExamenFisicoView, self).get_context_data(**kwargs)
        context.update({
            'ingreso': self.ingreso,
            'paciente': self.ingreso.paciente,
            'last_control': self.ingreso.embarazo.controles.last()
        })
        return context

    def form_valid(self, form):
        ef = form.save(commit=False)
        if ef.nivel_conciencia != ExamenFisico.NIVEL_CONCIENCIA_OTROS:
            ef.nivel_conciencia_otros = ''
        ef.save()
        return super(PExamenFisicoView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, u'Examen fisico guardado')
        return reverse('partos:partograma', kwargs={'ingreso_id': self.ingreso.id})

    def get_ingreso(self, **kwargs):
        try:
            ingreso = Ingreso.objects.get(id=kwargs.get('ingreso_id', 0))
            return ingreso
        except Ingreso.DoesNotExist:
            raise Http404


class ResumenPartoReportView(CanvasCommonMethodsMixin, PdfView):
    filename = 'resumen_parto_{}.pdf'
    partograma = None
    paciente = None
    usuario = None
    c = None
    data = None

    def get(self, request, *args, **kwargs):
        try:
            self.paciente = Paciente.objects.get(numero_documento=request.GET.get('dni_paciente', ''))
        except Paciente.DoesNotExist:
            messages.warning(request, 'No se ha encontrado paciente con el DNI: {}'.format(request.GET.get('dni_paciente')))
            return HttpResponseRedirect('/')
        self.partograma = Partograma.objects.filter(paciente_id=self.paciente.id).order_by('-created').first()
        if not self.partograma:
            messages.warning(request, 'No se ha encontrado partograma del paciente con DNI: {}'.format(request.GET.get('dni_paciente')))
            return HttpResponseRedirect('/')
        self.terminacion = TerminacionEmbarazo.objects.filter(ingreso_id=self.partograma.ingreso.id).order_by('-fecha' ,'-hora').first()
        if not self.terminacion:
            messages.warning(request, 'No se ha cerrado el partograma.')
            return HttpResponseRedirect('/')

        self.usuario = User.objects.filter(dni=self.terminacion.creator).first()
        if not self.usuario:
            messages.warning(request, 'Aún no se ha cerrado el partograma del paciente con DNI: {}'.format(request.GET.get('dni_paciente')))
            return HttpResponseRedirect('/')
        self.filename = self.filename.format(self.paciente.numero_documento)
        self.data = self.partograma.get_mediciones_dict()
        return super(ResumenPartoReportView, self).get(request, *args, **kwargs)

    def process_canvas(self, c):
        columnas = [30, 140, 230, 320, 410, 500]
        self.c = c
        self.header(columnas)
        self.block_periodo_1(columnas)
        self.block_periodo_2(columnas)
        self.block_periodo_3(columnas)
        self.block_periodo_4(columnas)

        c.showPage()
        return c

    def header(self, columnas):
        self.c.drawImage('static/img/logo_minsa.png', 15, 785, 127, 50)
        self.c.setFontSize(15)
        self.c.drawCentredString(298, 800, 'RESUMEN DE PARTO')
        self.c.setFontSize(7)
        self.c.drawString(columnas[0], 775, 'NOMBRE: {}'.format(
            self.paciente))
        self.c.drawString(columnas[0], 760, 'FECHA DE INGRESO: {}'.format(
            self.partograma.ingreso.fecha.strftime('%d/%m/%Y')))
        self.c.drawString(columnas[2], 760, 'HORA DE INGRESO: {}'.format(
            self.partograma.ingreso.hora.strftime('%H:%M')))
        historia = self.paciente.historias_clinicas.all().order_by('-modified').first()
        self.c.drawString(420, 760, 'Nº HISTORIA CLÍNICA: {}'.format(historia.numero))
        self.c.drawString(columnas[0], 745, 'FÓRMULA OBSTÉTRICA: ')
        self.c.drawString(columnas[1], 745, 'GRAVIDEZ:  {}'.format(self.paciente.ultimos_embarazos.count() + 1))
        self.c.drawString(columnas[2], 745, 'PARIDAD:  {}'.format(
            self.paciente.antecedente_obstetrico.partos if hasattr(self.paciente, 'antecedente_obstetrico') else 0))
        self.c.drawString(columnas[3], 745, 'FUM:  {}'.format(
            self.partograma.ingreso.embarazo.fum.strftime('%d/%m/%Y') if self.partograma.ingreso.embarazo.fum else ""))
        self.c.drawString(columnas[4], 745, 'EG:  {} ({})'.format(
            self.partograma.ingreso.edad_gestacional_semanas or " ", self.partograma.ingreso.eg_elegida.upper()))
        self.c.drawString(columnas[0], 730, 'MEMBRANAS:')
        ultima_medicion = self.partograma.mediciones.all().order_by('-fecha', '-hora').first()
        self.c.drawString(columnas[1], 730, 'ÍNTEGRAS {}'.format(
            "X" if ultima_medicion and ultima_medicion.tv_membranas == 'integras' else ""))
        self.c.drawString(columnas[2], 730, 'ROTAS {}'.format(
            "X" if ultima_medicion and ultima_medicion.tv_membranas == 'rotas' else ""))
        self.c.drawString(columnas[3], 730, 'HORAS: {}'.format(
            ultima_medicion.tv_membranas_rotas_tiempo if ultima_medicion and ultima_medicion.tv_membranas == 'rotas' else ""))

    def block_periodo_1(self, columnas):
        self.c.setFontSize(10)
        self.c.drawString(columnas[0], 715, 'PRIMER PERIODO')
        self.c.setFontSize(7)
        self.c.drawString(columnas[0], 700, 'TIEMPO: {} HORAS {} MINUTOS'.format(
            self.terminacion.duracion_parto_perdiodo_1_horas or " ",
            self.terminacion.duracion_parto_perdiodo_1_minutos or " "))

        self.c.drawString(columnas[0], 685, 'INICIO:')
        self.c.drawString(columnas[1], 685, 'ESPONTANEO {}'.format(
            "X" if self.terminacion.inicio_parto_periodo_1 == 'espontaneo' else ""
        ))
        self.c.drawString(columnas[2], 685, 'INDUCIDO {}'.format(
            "X" if self.terminacion.inicio_parto_periodo_1 == 'inducido' else ""
        ))
        self.c.drawString(columnas[3], 685, 'ESTIMULADO {}'.format(
            "X" if self.terminacion.inicio_parto_periodo_1 == 'estimulado' else ""
        ))

    def block_periodo_2(self, columnas):
        self.c.setFontSize(10)
        self.c.drawString(columnas[0], 665, 'SEGUNDO PERIODO')
        self.c.setFontSize(7)
        self.c.drawString(columnas[0], 650, 'TIEMPO: {} HORAS {} MINUTOS'.format(
            self.terminacion.duracion_parto_perdiodo_2_horas or " ",
            self.terminacion.duracion_parto_perdiodo_2_minutos or " "))
        self.c.drawString(columnas[0], 635, 'INICIO:')
        self.c.drawString(columnas[1], 635, 'ESPONTANEO {}'.format(
            "X" if self.terminacion.inicio_parto_periodo_2 == 'espontaneo' else ""
        ))
        self.c.drawString(columnas[2], 635, 'INDUCIDO {}'.format(
            "X" if self.terminacion.inicio_parto_periodo_2 == 'inducido' else ""
        ))
        self.c.drawString(columnas[3], 635, 'ESTIMULADO {}'.format(
            "X" if self.terminacion.inicio_parto_periodo_2 == 'estimulado' else ""
        ))
        self.c.drawString(columnas[0], 620, 'EPISIOTOMIA:')

        self.c.drawString(columnas[1], 620, 'NO {}'.format(
            "X" if not self.terminacion.tipo_episiotomia else ""
        ))
        self.c.drawString(columnas[2], 620, 'M {}'.format(
            "X" if self.terminacion.tipo_episiotomia == 'M' else ""
        ))
        self.c.drawString(columnas[3], 620, 'MLD {}'.format(
            "X" if self.terminacion.tipo_episiotomia == 'MLD' else ""
        ))
        self.c.drawString(columnas[4], 620, 'MLI {}'.format(
            "X" if self.terminacion.tipo_episiotomia == 'MLI' else ""
        ))
        self.c.drawString(columnas[0], 605, 'DESGARRO:')
        self.c.drawString(columnas[1], 605, 'I {}'.format(
            "X" if self.terminacion.desgarro_grado == '1' else ""
        ))
        self.c.drawString(columnas[2], 605, 'II {}'.format(
            "X" if self.terminacion.desgarro_grado == '2' else ""
        ))
        self.c.drawString(columnas[3], 605, 'III {}'.format(
            "X" if self.terminacion.desgarro_grado == '3' else ""
        ))
        self.c.drawString(columnas[4], 605, 'IV {}'.format(
            "X" if self.terminacion.desgarro_grado == '4' else ""
        ))
        self.c.drawString(columnas[0], 590, 'ÚNICO: {}'.format(
            "X" if self.terminacion.tipo == 'unico' else ""
        ))
        self.c.drawString(columnas[1], 590, 'MÚLTIPLE: {}'.format(
            "X" if self.terminacion.tipo == 'multiple' else ""
        ))
        self.c.drawString(columnas[0], 575, 'PARTOS:')
        if self.terminacion.fecha:
            self.c.drawString(columnas[1], 575, 'FECHA: {}'.format(
                self.terminacion.fecha))
        else:
            self.c.drawString(columnas[1], 575, 'FECHA: ')
        self.c.drawString(columnas[2], 575, 'HORA: {}'.format(
            self.terminacion.hora_1_parto_periodo_2.strftime('%H:%M')
            if self.terminacion.hora_1_parto_periodo_2 else ""))
        if self.terminacion.hora_2_parto_periodo_2:
            self.c.drawString(columnas[1], 560, 'FECHA: {}'.format(self.terminacion.fecha))
            self.c.drawString(columnas[2], 560, 'HORA: {}'.format(
                self.terminacion.hora_2_parto_periodo_2.strftime('%H:%M') if self.terminacion.hora_2_parto_periodo_2 else ""))
        if self.terminacion.hora_3_parto_periodo_2:
            self.c.drawString(columnas[1], 545, 'FECHA: {}'.format(self.terminacion.fecha))
            self.c.drawString(columnas[2], 545, 'HORA: {}'.format(
                self.terminacion.hora_3_parto_periodo_2.strftime('%H:%M') if self.terminacion.hora_3_parto_periodo_2 else ""))
        if self.terminacion.hora_4_parto_periodo_2:
            self.c.drawString(columnas[1], 530, 'FECHA: {}'.format(self.terminacion.fecha))
            self.c.drawString(columnas[2], 530, 'HORA: {}'.format(
                self.terminacion.hora_4_parto_periodo_2.strftime('%H:%M') if self.terminacion.hora_4_parto_periodo_2 else ""))
        if self.terminacion.hora_5_parto_periodo_2:
            self.c.drawString(columnas[1], 515, 'FECHA: {}'.format(self.terminacion.fecha))
            self.c.drawString(columnas[2], 515, 'HORA: {}'.format(
                self.terminacion.hora_5_parto_periodo_2.strftime('%H:%M') if self.terminacion.hora_5_parto_periodo_2 else ""))

    def block_periodo_3(self, columnas):
        self.c.setFontSize(10)
        self.c.drawString(columnas[0], 510, 'TERCER PERIODO')
        self.c.setFontSize(7)
        self.c.drawString(columnas[0], 495, 'HORA DE ALUMBRAMIENTO: {}'.format(
            self.terminacion.hora_parto_periodo_3.strftime('%H:%M')
            if self.terminacion.hora_parto_periodo_3 else ""))
        self.c.drawString(columnas[0], 480, 'DIRIGIDO: {}'.format(
            "SÍ" if self.terminacion.dirigido_parto_periodo_3 == 's' else "NO"))
        self.c.drawString(columnas[0], 465, 'PÉRDIDA SANGUINEA: {}'.format(self.terminacion.sangrado_aproximado + " mL"
            if self.terminacion.sangrado_aproximado is not None else ""))

    def block_periodo_4(self, columnas):
        placentas = self.terminacion.placentas.all()
        fila = 445
        self.c.setFontSize(10)
        self.c.drawString(columnas[0], fila, 'ANEXO')
        if placentas:
            for placenta in placentas:
                self.c.setFontSize(7)
                self.c.drawString(columnas[0], fila - 15, 'PLACENTA:')
                self.c.drawString(columnas[1], fila - 15, 'DIAMETROS: {} x {} cm'.format(
                    placenta.placenta_tamanio_ancho, placenta.placenta_tamanio_longitud))
                self.c.drawString(columnas[2], fila - 15, 'PESO: {} g'.format(placenta.placenta_peso))
                self.c.drawString(columnas[0], fila - 30, 'DESPRENDIMIENTO:')
                self.c.drawString(columnas[1], fila - 30, 'COMPLETO {}'.format(
                    "X" if placenta.placenta_desprendimiento == 'C' else ""))
                self.c.drawString(columnas[2], fila - 30, 'INCOMPLETO {}'.format(
                    "X" if placenta.placenta_desprendimiento == 'I' else ""))
                self.c.drawString(columnas[0], fila - 45, 'TIPO:')
                self.c.drawString(columnas[1], fila - 45, 'SHULTZ {}'.format(
                    "X" if placenta.placenta_tipo == 'shultz' else ""))
                self.c.drawString(columnas[2], fila - 45, 'DUNCAN {}'.format(
                    "X" if placenta.placenta_tipo == 'duncan' else ""))
                self.c.drawString(columnas[0], fila - 60, 'MEMBRANAS:')
                self.c.drawString(columnas[1], fila - 60, 'COMPLETO {}'.format(
                    "X" if placenta.membranas == 'C' else ""))
                self.c.drawString(columnas[2], fila - 60, 'INCOMPLETO {}'.format(
                    "X" if placenta.membranas == 'I' else ""))
                self.c.drawString(columnas[0], fila - 80, 'CORDÓN:')
                self.c.drawString(columnas[1], fila - 80, 'LONGITUD: {} cm'.format(placenta.cordon_umbilical_longitud
                    if placenta.cordon_umbilical_longitud is not None else ""))
                self.c.drawString(columnas[2], fila - 80, 'INSERCIÓN:')
                self.c.drawString(columnas[2]+50, fila - 80, 'CENTRAL {}'.format(
                    "X" if placenta.cordon_umbilical_insercion == 'central' else ""
                ))
                self.c.drawString(columnas[2]+100, fila - 80, 'EXCENTRICA {}'.format(
                    "X" if placenta.cordon_umbilical_insercion == 'excentrica' else ""
                ))
                self.c.drawString(columnas[2]+150, fila - 80, 'MARGINAL {}'.format(
                    "X" if placenta.cordon_umbilical_insercion == 'marginal (en raqueta)' else ""
                ))
                self.c.drawString(columnas[2]+200, fila - 80, 'VELAMENTOSA {}'.format(
                    "X" if placenta.cordon_umbilical_insercion == 'velamentosa' else ""
                ))
                self.c.drawString(columnas[0], fila - 95, 'CIRCULAR:')
                self.c.drawString(columnas[1], fila - 95, 'SIMPLE {}'.format(
                    "X" if placenta.cordon_umbilical_circular_tipo == 'simple' else ""
                ))
                self.c.drawString(columnas[2], fila - 95, 'DOBLE {}'.format(
                    "X" if placenta.cordon_umbilical_circular_tipo == 'doble' else ""
                ))
                self.c.drawString(columnas[3], fila - 95, 'TRIPLE {}'.format(
                    "X" if placenta.cordon_umbilical_circular_tipo == 'triple' else ""
                ))
                self.c.drawString(columnas[4], fila - 95, 'OTRO {}'.format(""))
                self.c.drawString(columnas[0], fila - 110, 'VASOS:')
                self.c.drawString(columnas[1], fila - 110, '1 VENA y 2 ARTERIAS {}'.format(
                    "X" if placenta.cordon_umbilical_vasos == '1 vena y 2 arterias' else ""
                ))
                self.c.drawString(columnas[2], fila - 110, 'OTROS {}'.format(
                    placenta.cordon_umbilical_otras_caracteristicas))
                self.c.drawString(columnas[0], fila - 130, 'LÍQUIDO AMNIÓTICO:')
                self.c.drawString(columnas[1], fila - 130, 'CANTIDAD {} ml:'.format(placenta.liquido_amniotico_cantidad
                    if placenta.liquido_amniotico_cantidad is not None else ""))
                self.c.drawString(columnas[2], fila - 130, 'COLOR:')
                self.c.drawString(columnas[3], fila - 130, 'CLARO {}'.format(
                    "X" if placenta.liquido_amniotico_color == 'claro' else ""
                ))
                self.c.drawString(columnas[4], fila - 130, 'MECONIAL {}'.format(
                    "X" if placenta.liquido_amniotico_color == 'meconial' else ""
                ))
                self.c.drawString(columnas[5], fila - 130, 'SANGUINOLENTO {}'.format(
                    "X" if placenta.liquido_amniotico_color == 'sanguinolento' else ""
                ))
                self.c.drawString(columnas[0], fila - 150, 'OTRAS CARACTERÍSTICAS: {}'.format(
                    "X" if placenta.otras_caracteristicas == 'claro' else ""
                ))
                self.c.drawString(columnas[0], fila - 165, '-----')
                fila -= 165
        else:
            self.c.setFontSize(7)
            self.c.drawString(columnas[0], fila - 15, 'PLACENTA:')
            self.c.drawString(columnas[1], fila - 15, 'DIAMETROS:')
            self.c.drawString(
                columnas[2], fila - 15, 'PESO:')
            self.c.drawString(columnas[0], fila - 30, 'DESPRENDIMIENTO:')
            self.c.drawString(columnas[1], fila - 30, 'COMPLETO')
            self.c.drawString(columnas[2], fila - 30, 'INCOMPLETO')
            self.c.drawString(columnas[0], fila - 45, 'TIPO:')
            self.c.drawString(columnas[1], fila - 45, 'SHULTZ')
            self.c.drawString(columnas[2], fila - 45, 'DUNCAN')
            self.c.drawString(columnas[0], fila - 60, 'MEMBRANAS:')
            self.c.drawString(columnas[1], fila - 60, 'COMPLETO')
            self.c.drawString(columnas[2], fila - 60, 'INCOMPLETO')
            self.c.drawString(columnas[0], fila - 80, 'CORDÓN:')
            self.c.drawString(
                columnas[1], fila - 80, 'LONGITUD:')
            self.c.drawString(columnas[2], fila - 80, 'INSERCIÓN:')
            self.c.drawString(columnas[2]+70, fila - 80, 'CENTRAL')
            self.c.drawString(columnas[2]+140, fila - 80, 'EXCENTRICA')
            self.c.drawString(columnas[2]+210, fila - 80, 'MARGINAL')
            self.c.drawString(columnas[2]+280, fila - 80, 'VELAMENTOSA')
            self.c.drawString(columnas[0], fila - 95, 'CIRCULAR:')
            self.c.drawString(columnas[1], fila - 95, 'SIMPLE')
            self.c.drawString(columnas[2], fila - 95, 'DOBLE')
            self.c.drawString(columnas[3], fila - 95, 'TRIPLE')
            self.c.drawString(columnas[4], fila - 95, 'OTRO')
            self.c.drawString(columnas[0], fila - 110, 'VASOS:')
            self.c.drawString(columnas[1], fila - 110, '1 VENA y 2 ARTERIAS')
            self.c.drawString(columnas[2], fila - 110, 'OTROS')
            self.c.drawString(columnas[0], fila - 130, 'LÍQUIDO AMNIÓTICO:')
            self.c.drawString(columnas[1], fila - 130, 'CANTIDAD:')
            self.c.drawString(columnas[2], fila - 130, 'COLOR:')
            self.c.drawString(columnas[3], fila - 130, 'CLARO')
            self.c.drawString(columnas[4], fila - 130, 'MECONIAL')
            self.c.drawString(columnas[5], fila - 130, 'SANGUINOLENTO')
            self.c.drawString(columnas[0], fila - 150, 'OTRAS CARACTERÍSTICAS:')
            self.c.drawString(columnas[0], fila - 165, '-----')
            fila -= 165

        fila -= 15
        self.c.setFontSize(10)
        self.c.drawString(columnas[0], fila, 'DURACIÓN DE PARTO')
        self.c.setFontSize(7)
        self.c.drawString(columnas[0], fila - 15, 'PRIMER PERIODO')
        self.c.drawString(columnas[1], fila - 15, 'TIEMPO: {} HORAS {} MINUTOS'.format(
            self.terminacion.duracion_parto_perdiodo_1_horas
            if self.terminacion.duracion_parto_perdiodo_1_horas is not None else "  ",
            self.terminacion.duracion_parto_perdiodo_1_minutos
            if self.terminacion.duracion_parto_perdiodo_1_minutos is not None else "  "))
        self.c.drawString(columnas[0], fila - 30, 'SEGUNDO PERIODO')
        self.c.drawString(columnas[1], fila - 30, 'TIEMPO: {} HORAS {} MINUTOS'.format(
            self.terminacion.duracion_parto_perdiodo_2_horas
            if self.terminacion.duracion_parto_perdiodo_2_horas is not None else "  ",
            self.terminacion.duracion_parto_perdiodo_2_minutos
            if self.terminacion.duracion_parto_perdiodo_2_minutos is not None else "  "))
        self.c.drawString(columnas[0], fila - 45, 'TERCER PERIODO')
        self.c.drawString(columnas[1], fila - 45, 'TIEMPO: {} HORAS {} MINUTOS'.format(
            self.terminacion.duracion_parto_perdiodo_3_horas
            if self.terminacion.duracion_parto_perdiodo_3_horas is not None else "  ",
            self.terminacion.duracion_parto_perdiodo_3_minutos
            if self.terminacion.duracion_parto_perdiodo_3_minutos is not None else "  "))

        self.c.setFontSize(7)
        self.c.drawString(columnas[0], fila - 85, 'RESPONSABLE DE LA ATENCIÓN: {}'.format(self.usuario.get_full_name()))

class PartogramaHomeReportView(CanvasCommonMethodsMixin, PdfView):
    filename = 'partograma_{}.pdf'
    partograma = None
    paciente = None
    usuario = None
    c = None
    data = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.paciente = Paciente.objects.get(numero_documento=request.GET.get('dni_paciente', ''))
        except Paciente.DoesNotExist:
            messages.warning(request, 'No se ha encontrado paciente con el DNI: {}'.format(request.GET.get('dni_paciente')))
            return HttpResponseRedirect('/')
        self.partograma = Partograma.objects.filter(paciente_id=self.paciente.id).order_by('-created').first()
        if not self.partograma:
            messages.warning(request, 'No se ha encontrado partograma con el DNI: {}'.format(request.GET.get('dni_paciente')))
            return HttpResponseRedirect('/')
        self.usuario = get_object_or_404(User, dni=self.partograma.created_by)
        self.filename = self.filename.format(self.paciente.numero_documento)
        self.data = self.partograma.get_mediciones_dict()
        self.ingreso = get_object_or_404(Ingreso, id=self.partograma.ingreso_id)
        return super(PartogramaHomeReportView, self).dispatch(request, *args, **kwargs)

    def process_canvas(self, c):
        self.c = c
        self._calculate_base_x()
        self.header()
        self.block1()
        self.block2()
        self.c.setLineWidth(0.5)
        self.block3()
        self.block4()
        c.setFontSize(5)
        for val in range(11):
            c.drawString(210, 520 + val * 7, str(val).rjust(3, b' '))
        for val in range(1, 6):
            c.drawString(210, 445 + val * 7, str(val).rjust(3, b' '))
        values = tuple(range(60, 180, 10))
        for val in range(12):
            c.drawString(205, 270 + val * 7, str(values[val]).rjust(3, b' '))
        c.drawString(188, 515, 'Nº HORAS')
        c.drawString(195, 508, 'HORAS')
        c.showPage()
        return c

    def _calculate_base_x(self):
        self.base_x = 230
        try:
            dilatacion = int(self.data[1]['dilatacion'])
            if dilatacion >= 4:
                self.base_x += (dilatacion - 4) * 24
        except ValueError:
            pass

    def grid(self, x=0, y=0, rows=1, cols=1, w=10, h=10):
        for i in range(cols):
            for j in range(rows):
                path = self.c.beginPath()
                _x = i * w + x
                _y = j * h + y
                path.moveTo(_x, _y)
                path.lineTo(_x, _y + h)
                path.lineTo(_x + w, _y + h)
                path.lineTo(_x + w, _y)
                path.lineTo(_x, _y)
                self.c.drawPath(path)

    def draw_rect_stripped(self, x, y, w, h, sep=1):
        self.c.rect(x, y, w, h)
        p1 = []
        p2 = []
        for i in range(y + h, y, -sep):
            p1.append(Point(x=x, y=i))
        for i in range(x, x + w, sep):
            p1.append(Point(x=i, y=y))
            p2.append(Point(x=i, y=y + h))
        for i in range(y + h, y, -sep):
            p2.append(Point(x=x + w, y=i))
        for i in range(len(p1)):
            self.c.line(p1[i].x, p1[i].y, p2[i].x, p2[i].y)

    def draw_rect_circle(self, x, y, w, h, sep=1):
        self.c.rect(x, y, w, h)
        r = 1
        for i in range(x + r + r / 2, x + w, r * 2 + 1):
            for j in range(y + r + r / 2, y + h, r * 2 + 1):
                self.c.circle(i + r / 2.0, j + r / 2.0, r, stroke=0, fill=1)

    def draw_diagonal_text(self, x, y, angle, size, text):
        self.c.saveState()
        self.c.translate(x, y)
        self.c.rotate(angle)
        self.c.setFontSize(size)
        self.c.setFillColor('gray')
        self.c.drawString(0, 0, text)
        self.c.restoreState()

    def header(self):
        self.c.drawImage('static/img/logo_minsa.png', 15, 785, 127, 50)
        self.c.setFontSize(15)
        self.c.drawCentredString(298, 800, 'PARTOGRAMA DE LA OMS MODIFICADO')
        self.c.setFontSize(7)
        self.c.drawString(30, 780, 'NOMBRE: ')
        self.c.setFontSize(6)
        self.c.drawString(70, 780, '{}'.format(self.paciente.nombre_completo))
        self.c.setFontSize(7)
        self.c.drawString(250, 780, 'GRAVIDEZ: {}'.format(
            self.paciente.ultimos_embarazos.count() + 1))
        self.c.drawString(310, 780, 'PARIDAD: {}'.format(
            self.paciente.antecedente_obstetrico.partos if hasattr(self.paciente, 'antecedente_obstetrico') else 0))
        historia = self.paciente.historias_clinicas.all().order_by('-modified').first()
        self.c.drawString(370, 780, 'Nº HISTORIA CLÍNICA: {}'.format(historia.numero))
        self.c.drawString(30, 765, 'FECHA DE INGRESO: {}'.format(
            self.partograma.ingreso.fecha.strftime('%d/%m/%Y')))
        self.c.drawString(200, 765, 'HORA DE INGRESO: {}'.format(
            self.partograma.ingreso.hora.strftime('%H:%M')))
        medicion_membrana_rota = self.partograma.mediciones.filter(
            tv_membranas='rotas').order_by('hora').first()
        hora = ''
        minutos = ''
        if self.ingreso.tiempo_ruptura_membranas_horas:
            hora = '{} H'.format(self.ingreso.tiempo_ruptura_membranas_horas)
        if self.ingreso.tiempo_ruptura_membranas_minutos:
            minutos = '{} min'.format(self.ingreso.tiempo_ruptura_membranas_minutos)
        self.c.drawString(350, 765, 'TIEMPO DE MEMBRANAS ROTAS: {} {}'.format(hora, minutos))

    def block1(self):
        self.c.setLineWidth(0.5)
        self.grid(x=220, y=640, rows=13, cols=24, w=12, h=7)
        self.grid(x=220, y=620, rows=2, cols=24, w=12, h=7)

        self.c.setFontSize(7)
        self.c.drawString(20, 700, 'FCF')
        self.c.drawString(20, 670, 'INTEGRAS: I')
        self.c.drawString(20, 660, 'ROTAS: R')
        self.c.drawString(20, 650, 'LIQ. CLARO: C')
        self.c.drawString(20, 640, 'LIQ. MECONIAL: M')
        self.c.drawString(20, 630, 'LIQ. SANGUINOLENTO: S')
        self.c.setFontSize(6)
        self.c.drawString(150, 630, 'Líquido amniótico')
        self.c.drawString(150, 620, 'Moldeaminetos')
        self.c.setFontSize(5)
        values = tuple(range(80, 210, 10))
        for val in range(13):
            self.c.drawString(205, 639.5 + val * 7, str(values[val]).rjust(3, b' '))

        self.c.setFontSize(6)
        moldeaminetos_base = Point(self.base_x - 5, 622)
        liquido_amniotico_base = Point(self.base_x - 5, 629)
        fcf_init = Point(self.base_x - 10, 640)

        puntos = None
        contador = 0
        for index in range(24):
            self.c.drawString(moldeaminetos_base.x + 12 * index, moldeaminetos_base.y,
                              self.data[index + 1]['moldeaminetos'] or '')
            self.c.drawString(liquido_amniotico_base.x + 12 * index, liquido_amniotico_base.y,
                              self.data[index + 1]['liquido_amniotico'] or '')
            _fcf = self.data[index + 1]['fcf']

            if _fcf:
                _fcf_split = _fcf.split()
                if contador == 0:
                    puntos = [[] for i in range(len(_fcf_split))]
                    contador += 1
                for i in range(0, len(_fcf_split)):
                    puntos[i].append((fcf_init.x + 12 * index, fcf_init.y + ((int(_fcf_split[i]) - 80) / 10.0) * 7))

        if puntos:
            self.c.setLineWidth(1.5)
            for elemento in puntos:
                path = self.c.beginPath()
                path.moveTo(elemento[0][0], elemento[0][1])
                for _x, _y in elemento[1:]:
                    path.lineTo(_x, _y)
                self.c.setStrokeColor('blue')
                self.c.drawPath(path)
                self.c.setStrokeColor('black')

    def block2(self):
        self.c.setLineWidth(0.5)
        self.grid(x=220, y=520, rows=10, cols=24, w=12, h=7)
        self.grid(x=220, y=506, rows=2, cols=12, w=24, h=7)
        self.draw_diagonal_text(255, 562, 18, 12, 'ALERTA')
        self.draw_diagonal_text(390, 556, 16, 12, 'ACCIÓN')

        self.c.setLineWidth(1)

        self.c.line(220, 548, 364, 590)
        self.c.line(316, 548, 460, 590)

        self.c.line(40, 590, 60, 590)
        self.c.line(50, 520, 50, 550)
        self.c.line(50, 565, 50, 590)
        self.c.line(40, 520, 60, 520)
        self.c.setFontSize(4)
        self.c.drawCentredString(50, 560, 'CUELLO UTERINO (CM)')
        self.c.drawCentredString(50, 553, 'TRAZO X')

        self.c.line(120, 570, 140, 570)
        self.c.line(130, 520, 130, 535)
        self.c.line(130, 550, 130, 570)
        self.c.line(120, 520, 140, 520)

        self.c.drawCentredString(130, 545, 'DESCENSO CEFALICO')
        self.c.drawCentredString(130, 538, '(TRAZO O)')

        dilatacion_points = []
        descenso_cefalico_points = []

        init = Point(self.base_x - 10, 520)

        # Print hours

        self.c.saveState()
        self.c.setFontSize(6)
        for i in range(0, 12):
            self.c.drawString(230 + i * 24, 514, str(i + 1))
        for i in range(0, 12):
            if self.base_x + i * 24 > 320 + 8 * 24:
                continue
            hora_key = i * 2 + 1
            self.c.drawString(self.base_x + i * 24 - 6, 508, self.data[hora_key].get('hora', ''))

        self.c.restoreState()

        for index in range(24):
            dilatacion = self.data[index + 1]['dilatacion']
            descenso_cefalico = self.data[index + 1]['descenso_cefalico']
            if dilatacion and isinstance(dilatacion, int):
                dilatacion = int(dilatacion)
                dilatacion_points.append((init.x + 12 * index, init.y + dilatacion * 7))
            if descenso_cefalico and isinstance(descenso_cefalico, int):
                descenso_cefalico = int(descenso_cefalico)
                descenso_cefalico_points.append((init.x + 12 * index, init.y + descenso_cefalico * 7))

        if dilatacion_points:
            self.c.setLineWidth(1.5)
            path = self.c.beginPath()
            path.moveTo(dilatacion_points[0][0], dilatacion_points[0][1])
            self.draw_x(dilatacion_points[0][0], dilatacion_points[0][1], size=2)
            for _x, _y in dilatacion_points[1:]:
                path.lineTo(_x, _y)
                self.draw_x(_x, _y, size=2)
            self.c.setStrokeColor('red')
            self.c.drawPath(path)
            self.c.setStrokeColor('black')

        if descenso_cefalico_points:
            self.c.setLineWidth(1.5)
            path = self.c.beginPath()
            path.moveTo(descenso_cefalico_points[0][0], descenso_cefalico_points[0][1])
            self.c.setFillColorRGB(0, 0, 0)
            self.c.circle(descenso_cefalico_points[0][0], descenso_cefalico_points[0][1], 2, stroke=0, fill=1)
            for _x, _y in descenso_cefalico_points[1:]:
                path.lineTo(_x, _y)
                self.c.setFillColorRGB(0, 0, 0)
                self.c.circle(_x, _y, 2, stroke=0, fill=1)
            self.c.setStrokeColor('blue')
            self.c.drawPath(path)
            self.c.setStrokeColor('black')

    def block3(self):
        self.grid(x=220, y=450, rows=5, cols=24, w=12, h=7)

        self.grid(x=220, y=420, rows=2, cols=24, w=12, h=7)
        self.c.setFontSize(5)
        self.c.drawString(50, 475, 'MENOR DE 20')
        self.draw_rect_circle(90, 473, 12, 7)
        self.c.drawString(50, 465, 'ENTRE 20 Y 40')
        self.draw_rect_stripped(90, 463, 12, 7, sep=4)
        self.c.drawString(50, 455, 'MAYOR DE 40')
        self.c.rect(90, 453, 12, 7, stroke=1, fill=1)

        self.c.setFontSize(5)
        self.c.drawString(180, 429, 'OXITOCINA UL')
        self.c.drawString(180, 422, 'GOTAS / MIN.')
        init = Point(x=self.base_x - 8, y=422)
        self.c.setFillColorRGB(0, 0, 0)
        for index in range(24):
            goteo = self.data[index + 1]['goteo']
            oxitocina = self.data[index + 1]['oxitocina']
            duracion = self.data[index + 1]['duracion']
            frecuencia = self.data[index + 1]['frecuencia']
            if oxitocina:
                self.c.drawString(init.x + 12 * index, init.y + 7, oxitocina)
            if goteo:
                self.c.drawString(init.x + 12 * index, init.y, goteo)

            if frecuencia in ('1/10', '2/10', '3/10', '4/10', '5+/10') and duracion:
                frecuencia = int(frecuencia[0])
                if duracion == '40+':
                    self.c.rect(init.x - 2 + 12 * index, init.y + 28, 12, 7 * frecuencia, stroke=0, fill=1)
                elif duracion == '-20':
                    self.draw_rect_circle(init.x - 2 + 12 * index, init.y + 28, 12, 7 * frecuencia, sep=4)
                else:
                    self.draw_rect_stripped(init.x - 2 + 12 * index, init.y + 28, 12, 7 * frecuencia, sep=4)

    def block4(self):
        self.c.setLineWidth(0.5)
        self.grid(x=220, y=270, rows=17, cols=24, w=12, h=7)

        self.grid(x=220, y=240, rows=1, cols=24, w=12, h=7)

        self.grid(x=220, y=210, rows=3, cols=24, w=12, h=7)

        self.c.drawCentredString(60, 370, 'PULSO')
        self.c.circle(60, 365, 2, stroke=1, fill=1)
        self.c.drawCentredString(50, 333, 'PRESION')
        self.c.drawCentredString(50, 323, 'ARTERIAL')
        self.draw_arrow(75, 310, 75, 345)

        self.c.drawString(70, 240, 'TEMPERATURA')

        self.c.drawString(70, 220, 'ORINA')
        path = self.c.beginPath()
        path.moveTo(105, 231)
        path.lineTo(103, 229)
        path.lineTo(103, 223)
        path.lineTo(101, 221)
        path.lineTo(103, 219)
        path.lineTo(103, 213)
        path.lineTo(105, 211)
        self.c.drawPath(path)
        self.c.drawString(110, 227, 'PROTEINA')
        self.c.drawString(110, 220, 'ACETONA')
        self.c.drawString(110, 213, 'VOLUMEN')

        self.c.setFontSize(10)
        self.c.drawString(70, 150, 'RESPONSABLE DE LA ATENCIÓN: {}'.format(self.usuario.get_full_name()))

        pulso_points = []
        init = Point(x=self.base_x - 10, y=270)

        temp_init = Point(x=self.base_x - 9, y=242)
        orin_init = Point(x=self.base_x - 9, y=212)
        self.c.setFontSize(5)
        self.c.setLineWidth(1.5)
        for index in range(24):
            self.c.drawString(temp_init.x + 12 * index, temp_init.y, str(
                self.data[index + 1]['temperatura']) or '')
            self.c.drawString(orin_init.x + 12 * index, orin_init.y + 12.5, str(
                self.data[index + 1]['orina_proteinas']) or '')
            self.c.drawString(orin_init.x + 12 * index, orin_init.y + 6.5, str(
                self.data[index + 1]['orina_cetona']) or '')
            self.c.drawString(orin_init.x + 12 * index, orin_init.y, str(
                self.data[index + 1]['orina_volumen']) if self.data[index + 1]['orina_volumen'] is not None else '')
            pulso = self.data[index + 1]['pulso']
            sistolica = self.data[index + 1]['sistolica']
            diastolica = self.data[index + 1]['diastolica']
            if pulso:
                pulso_points.append(
                    Point(x=init.x + 12 * index, y=init.y + ((pulso - 60) / 10.0) * 7))
            if sistolica and diastolica:
                self.draw_arrow(init.x + 12 * index + 6, init.y + ((diastolica - 60) / 10.0) * 7,
                                init.x + 12 * index + 6, init.y + ((sistolica - 60) / 10.0) * 7)

        if pulso_points:
            path = self.c.beginPath()
            first_point = pulso_points[0]
            path.moveTo(first_point.x, first_point.y)
            self.c.circle(first_point.x, first_point.y, 2, stroke=0, fill=1)
            for _x, _y in pulso_points[1:]:
                path.lineTo(_x, _y)
                self.c.circle(_x, _y, 2, stroke=0, fill=1)
            self.c.setStrokeColor('red')
            self.c.drawPath(path)
            self.c.setStrokeColor('black')


class ReferidasView(EstablecimientoRequiredMixin, ListView):
    template_name = 'partos/referidas.html'
    model = TerminacionEmbarazo
    paginate_by = 10
    context_object_name = 'terminaciones'

    def get_queryset(self):
        hoy = datetime.now()
        qs = super(ReferidasView, self).get_queryset()
        qs = qs.filter(establecimiento_id=self.request.session[
                       'establecimiento_id']).filter(referido='s').filter(
                           created__year=hoy.year, created__month=hoy.month)
        return qs

    def traer_hc(self):
        establecimiento_id = self.request.session['establecimiento_id']
        return HistoriaClinica.objects.get(establecimiento_id=establecimiento_id, paciente_id=1).numero

    def get_context_data(self, **kwargs):
        context = super(ReferidasView, self).get_context_data(**kwargs)
        context['menu'] = 'referida'
        return context
