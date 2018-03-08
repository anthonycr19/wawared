# coding:utf-8
import json
import random

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.db import transaction, IntegrityError, connection
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.http.response import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    CreateView, ListView, UpdateView, DetailView, View, TemplateView, FormView)

from cie.models import ICD10, ICD10Medical
from dashboard.views import (
    EstablecimientoRequiredMixin, HistoriaClinicaRequiredMixin)
from embarazos.models import UltimoEmbarazo
from establecimientos.models import Establecimiento
from partos.models import Ingreso

from .forms import (
    PacienteForm, AntecedenteGinecologicoForm, VacunaForm, VacunaPreForm, HistoriaClinicaForm)
from .models import (
    Paciente, RelacionParentesco, AntecedenteFamiliar, AntecedenteMedico,
    AntecedenteObstetrico, Vacuna, HistoriaClinica)
from ciudadano import CiudadanoRest

User = get_user_model()


class HistoriaClinicaCreateView(EstablecimientoRequiredMixin, CreateView):
    template_name = 'pacientes/historia_clinica_register.html'
    model = HistoriaClinica
    form_class = HistoriaClinicaForm
    permissions = ('pacientes.add_historiaclinica',)

    def dispatch(self, request, *args, **kwargs):
        self.paciente = get_object_or_404(
            Paciente, id=kwargs.get('paciente_id', None))
        self.establecimiento = get_object_or_404(
            Establecimiento, id=request.session['establecimiento_id'])
        return super(
            HistoriaClinicaCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            with transaction.atomic():
                self.object = form.save(commit=False)
                self.object.paciente = self.paciente
                self.object.establecimiento = self.establecimiento
                self.object.save()
                messages.success(
                    self.request, u'Número de historia clinica creada')
                return HttpResponseRedirect(self.get_success_url())
        except IntegrityError:
            messages.warning(
                self.request, u'Error: El número de historia clínica debe ser '
                              u'único por establecimiento y paciente')
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(
            HistoriaClinicaCreateView, self).get_context_data(**kwargs)
        context.update({
            'paciente': self.paciente,
            'establecimiento': self.establecimiento
        })
        return context

    def get_success_url(self):
        return reverse('paciente:update', kwargs={'id': self.paciente.id})


class PacienteCreateView(EstablecimientoRequiredMixin, CreateView):
    template_name = 'pacientes/paciente_register.html'
    model = Paciente
    form_class = PacienteForm
    permissions = ('pacientes.add_paciente',)

    def get_context_data(self, **kwargs):
        context = super(PacienteCreateView, self).get_context_data(**kwargs)
        context['menu'] = 'registrar'
        return context

    def get_form(self, form_class):
        form = super(PacienteCreateView, self).get_form(form_class)
        form.set_establecimiento_id(self.request.session['establecimiento_id'])
        return form

    def form_valid(self, form):

        self.object = form.save()

        if (
                self.object.tipo_documento == 'nodoc' or self.object.tipo_documento == 'notrajo') and self.object.numero_documento == '#temp#':
            self.object.numero_documento = 'SD-{0}'.format(self.object.id)
            self.object.save()

        HistoriaClinica.objects.create(
            numero=form.cleaned_data['hc'],
            establecimiento_id=self.request.session['establecimiento_id'],
            paciente=self.object
        )
        contrasena = random.randrange(10000, 99999)
        apellidos = self.object.apellido_paterno + ' '
        apellidos += self.object.apellido_materno

        if self.object.email is None or self.object.email == '':
            email_tmp = u'info@wawared.org'
        else:
            email_tmp = self.object.email

        documento_tmp = self.object.numero_documento
        if self.object.numero_documento is None or \
                self.object.numero_documento == '':
            documento_tmp = self.object.dni_responsable

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, u'Gestante registrada')
        return reverse(
            'paciente:antecedentes_edit', kwargs={'id': self.object.id})


class PacienteDetailView(EstablecimientoRequiredMixin, UpdateView):
    template_name = 'pacientes/paciente_edit.html'
    form_class = PacienteForm
    model = Paciente
    pk_url_kwarg = 'id'
    context_object_name = 'paciente'
    paciente_key = 'id'

    def post(self, request, *args, **kwargs):
        return HttpResponseNotAllowed('')


class PacienteUpdateView(EstablecimientoRequiredMixin, HistoriaClinicaRequiredMixin, UpdateView):
    template_name = 'pacientes/paciente_edit.html'
    model = Paciente
    form_class = PacienteForm
    pk_url_kwarg = 'id'
    context_object_name = 'paciente'
    paciente_key = 'id'
    permissions = ('pacientes.change_paciente',)

    def get_form(self, form_class):
        form = super(PacienteUpdateView, self).get_form(form_class)
        form.set_establecimiento_id(self.request.session['establecimiento_id'])
        form.set_hc_value()
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        historia_clinica = HistoriaClinica.objects.get(
            establecimiento_id=self.request.session['establecimiento_id'],
            paciente_id=self.object.id)
        historia_clinica.numero = form.cleaned_data['hc']
        historia_clinica.save()
        self.object.save()
        return super(PacienteUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(
            self.request, u'Los datos de la gestante fueron actualizados')
        return reverse(
            'paciente:antecedentes_edit', kwargs={'id': self.object.id})

    def urlback(self):
        return self.request.META.get('HTTP_REFERER')


class PacienteControlUpdateView(EstablecimientoRequiredMixin, HistoriaClinicaRequiredMixin, UpdateView):
    template_name = 'pacientes/paciente_control_edit.html'
    model = Paciente
    form_class = PacienteForm
    pk_url_kwarg = 'id'
    context_object_name = 'paciente'
    paciente_key = 'id'
    permissions = ('pacientes.change_paciente',)

    def get_form(self, form_class):
        form = super(PacienteControlUpdateView, self).get_form(form_class)
        form.set_establecimiento_id(self.request.session.get('establecimiento_id'))
        form.set_hc_value()
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        try:
            historia_clinica = HistoriaClinica.objects.get(
                establecimiento_id=self.request.session.get('establecimiento_id'),
                paciente_id=self.object.id)
            historia_clinica.numero = form.cleaned_data['hc']
            historia_clinica.save()
            self.object.save()
        except HistoriaClinica.DoesNotExist:
            pass
        return super(PacienteControlUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(
            self.request, u'Los datos de la gestante fueron actualizados')
        return reverse(
            'paciente:control_antecedentes_edit', kwargs={'id': self.object.id})

    def urlback(self):
        return self.request.META.get('HTTP_REFERER')


class PacienteSearchView(EstablecimientoRequiredMixin, ListView):
    template_name = 'pacientes/paciente_list.html'
    model = Paciente
    paginate_by = settings.PAGE_SIZE
    context_object_name = 'pacientes'

    def get(self, request, *args, **kwargs):
        establecimiento_actual = Establecimiento.objects.get(id=self.request.session['establecimiento_id'])

        q = self.request.GET.get(u'q', u'')
        q2 = self.request.GET.get(u'q2', u'')
        t = self.request.GET.get(u't', u'')
        resultados = []

        if q or q2:
            if t == '1':

                if not establecimiento_actual.modulo_citas:

                    paciente = Paciente.objects.filter(tipo_documento='dni', numero_documento=q).first()

                    if paciente:
                        resultados.append(paciente)
                    else:
                        paciente = CiudadanoRest().get_persona_por_dni(q)

                        if paciente:
                            resultados.append(paciente)
                        else:
                            resultados.append(
                                'Paciente no encontrado, la consulta RENIEC esta presentando '
                                'algunos problemas intente nuevamente ')
                else:
                    try:
                        paciente = Paciente.objects.filter(tipo_documento='dni', numero_documento=q).first()

                        if paciente:
                            resultados.append(paciente)
                        else:

                            # '01'--> tipo documento DNI
                            paciente = CiudadanoRest().get_persona_por_tipo_documento('01', q,
                                                                                      establecimiento_actual.codigo)

                            if paciente:

                                with transaction.atomic():
                                    paciente.save()
                                    HistoriaClinica.objects.create(
                                        numero=paciente.numero_documento,
                                        establecimiento_id=establecimiento_actual.id,
                                        paciente=paciente
                                    )
                                    resultados.append(paciente)
                            else:
                                resultados.append(
                                    'Paciente no encontrado, afiliar al paciente en el módulo de admisión')
                    except Exception as e:
                        resultados = None

            elif t == '2':
                params = ('%' + q + '%').upper()
                params2 = ('%' + q2 + '%').upper()
                cursor = connection.cursor()

                sql = """select p.id
                        from pacientes_paciente as p
                        where upper(p.nombres) like %s and upper(p.apellido_paterno || ' ' || p.apellido_materno) like %s; """

                cursor.execute(sql, [params, params2])

                ids = (row[0] for row in cursor.fetchall())
                resultados = self.model.objects.filter(id__in=ids)
            elif t == '3':

                if not establecimiento_actual.modulo_citas:
                    params = q.upper()
                    cursor = connection.cursor()

                    sql = """select p.id from pacientes_paciente as p where p.tipo_documento<>'dni' and upper(p.numero_documento)=%s;"""
                    cursor.execute(sql, (params,))
                    ids = (row[0] for row in cursor.fetchall())
                    resultados = self.model.objects.filter(id__in=ids)
                else:
                    # '10'--> tipos documentos diferente a DNI
                    paciente = CiudadanoRest().get_persona_por_tipo_documento('10', q, establecimiento_actual.codigo)

                    if paciente:
                        resultados.append(paciente)
                    else:
                        resultados.append('Paciente no encontrado, afiliar al paciente en el módulo de admisión')

        self.object_list = resultados
        if resultados:
            if not isinstance(resultados[0], str):
                for elemento in resultados:
                    if elemento.embarazos:
                        for embarazo in elemento.embarazos.filter(activo=True):
                            try:
                                ingreso = Ingreso.objects.get(embarazo_id=embarazo.id,paciente_id=elemento.id)
                                elemento.ingreso = ingreso.id
                            except:
                                elemento.ingreso = None
                    if elemento.terminaciones_embarazo:
                        try:
                            terminacion = elemento.terminaciones_embarazo.all().order_by("-fecha", "-hora").first()
                            elemento.terminacion_embarazo = terminacion
                        except:
                            elemento.terminacion_embarazo = None

        return self.render_to_response(
            self.get_context_data(pacientes=resultados))

    def get_context_data(self, **kwargs):
        context = super(PacienteSearchView, self).get_context_data(**kwargs)
        total = 0
        msg = ''

        if context['pacientes']:
            t = self.request.GET.get(u't', u'')

            if t == '1' or t == '3':
                pacientes = context['pacientes']
                total = len(pacientes)

                if not isinstance(pacientes[0], int):
                    paciente = pacientes[0]
                else:
                    total -= 1
                    paciente = pacientes[1]

                if not isinstance(paciente, Paciente):
                    msg = paciente
                    context['pacientes'] = None
                    total = 0
            else:
                pacientes = context['pacientes']
                total = len(pacientes)

        context.update({
            'menu': 'buscar',
            'total': total,
            'msg': msg,
            'query': u't={}&q={}&q2={}'.format(self.request.GET.get(u't', u''), self.request.GET.get(u'q', u''),
                                               self.request.GET.get(u'q2', u'')),
            'modulo_parto': self.request.session.get('modulo_parto', False),
            'estado_partograma': 'abierto'
        })
        context['menu'] = 'buscar'

        return context


class PacienteCreateForce(EstablecimientoRequiredMixin, FormView):
    def get(self, request, *args, **kwargs):

        dni = kwargs['id']

        paciente = Paciente.objects.filter(tipo_documento='dni', numero_documento=dni).first()

        if paciente is None:
            paciente = CiudadanoRest().get_persona_por_dni(dni)
            paciente.save()

        try:
            hc = HistoriaClinica.objects.get( \
                establecimiento=Establecimiento.objects.get(id=self.request.session['establecimiento_id']), numero=dni)
        except Exception as e:
            hc = HistoriaClinica()
            hc.numero = dni
            establecimiento = Establecimiento.objects.get(id=self.request.session['establecimiento_id'])
            hc.establecimiento = establecimiento

        hc.paciente = paciente
        hc.save()

        return HttpResponseRedirect(reverse('paciente:update', kwargs={'id': paciente.id}))


class PacienteCreateForceUpdate(EstablecimientoRequiredMixin, FormView):
    def get(self, request, *args, **kwargs):
        dni = kwargs['id']
        paciente = Paciente.objects.filter(tipo_documento='dni', numero_documento=dni).first()
        if paciente is None:
            paciente = CiudadanoRest().get_persona_por_dni(dni)
            paciente.save()

        try:
            hc = HistoriaClinica.objects.get(establecimiento=Establecimiento.objects.get(
                id=self.request.session.get('establecimiento_id')), numero=dni)
        except HistoriaClinica.DoesNotExist:
            hc = HistoriaClinica()
            hc.numero = dni
            establecimiento = Establecimiento.objects.get(id=self.request.session.get('establecimiento_id'))
            #El establecimento siempre va existir para poder ingresar a cualquier módulo
            hc.establecimiento = establecimiento
        hc.paciente = paciente
        hc.save()

        return HttpResponseRedirect(reverse('partos:paciente_control_update', kwargs={'id': paciente.id}))


class PacienteAntecedentesDetailView(EstablecimientoRequiredMixin, HistoriaClinicaRequiredMixin, UpdateView):
    template_name = 'pacientes/antecedentes.html'
    model = AntecedenteObstetrico
    form_class = AntecedenteGinecologicoForm
    paciente = None
    object = None
    paciente_key = 'id'

    def dispatch(self, request, *args, **kwargs):
        try:
            paciente = Paciente.objects.get(id=kwargs.get('id', 0))
            self.paciente = paciente
            return super(PacienteAntecedentesDetailView, self).dispatch(
                request, *args, **kwargs)
        except Paciente.DoesNotExist:
            raise Http404

    def get_object(self, queryset=None):
        return self.paciente.antecedente_ginecologico

    def get_context_data(self, **kwargs):
        context = super(
            PacienteAntecedentesDetailView, self).get_context_data(**kwargs)
        context.update({
            'ultimos_embarazos': self.get_ultimos_embarazos(),
            'paciente': self.paciente,
            'vacuna_form': self.get_vacuna_form()
        })
        return context

    def get_ultimos_embarazos(self):
        return UltimoEmbarazo.objects.filter(
            paciente=self.paciente).order_by('numero')

    def get_vacuna_form(self):
        vacuna, _ = Vacuna.objects.get_or_create(paciente=self.paciente)
        form = VacunaPreForm(self.request.POST or None, instance=vacuna)
        return form


class PacienteControlAntecedentesDetailView(EstablecimientoRequiredMixin, HistoriaClinicaRequiredMixin, UpdateView):
    template_name = 'pacientes/control_antecedentes.html'
    form_class = AntecedenteGinecologicoForm
    paciente = None
    object = None

    def dispatch(self, request, *args, **kwargs):
        self.paciente = get_object_or_404(Paciente, id=kwargs.get('id', 0))
        return super(PacienteControlAntecedentesDetailView, self).dispatch(
            request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return HttpResponseNotAllowed('')

    def get_object(self, queryset=None):
        return self.paciente.antecedente_ginecologico

    def get_context_data(self, **kwargs):
        context = super(
            PacienteControlAntecedentesDetailView, self).get_context_data(**kwargs)
        context.update({
            'ultimos_embarazos': self.get_ultimos_embarazos(),
            'paciente': self.paciente,
            'vacuna_form': self.get_vacuna_form()
        })
        return context

    def get_ultimos_embarazos(self):
        return UltimoEmbarazo.objects.filter(
            paciente=self.paciente).order_by('numero')

    def get_vacuna_form(self):
        vacuna, created = Vacuna.objects.get_or_create(paciente=self.paciente)
        form = VacunaPreForm(self.request.POST or None, instance=vacuna)
        return form


class PacienteAntecedentesUpdateView(EstablecimientoRequiredMixin, HistoriaClinicaRequiredMixin,
                                     UpdateView):
    template_name = 'pacientes/antecedentes.html'
    model = AntecedenteObstetrico
    form_class = AntecedenteGinecologicoForm
    paciente = None
    object = None
    paciente_key = 'id'
    permissions = ('pacientes.change_antecedenteginecologico',)

    def dispatch(self, request, *args, **kwargs):
        try:
            paciente = Paciente.objects.get(id=kwargs.get('id', 0))
            self.paciente = paciente
            return super(PacienteAntecedentesUpdateView, self).dispatch(
                request, *args, **kwargs)
        except Paciente.DoesNotExist:
            raise Http404

    def post(self, request, *args, **kwargs):
        form = self.form_class(
            self.request.POST or None, instance=self.get_object())
        vacuna_form = self.get_vacuna_form()
        if form.is_valid() and vacuna_form.is_valid():
            return self.form_valid(form, vacuna_form)
        else:
            return self.form_invalid(form, vacuna_form)

    def get_object(self, queryset=None):
        return self.paciente.antecedente_ginecologico

    def get_context_data(self, **kwargs):
        context = super(
            PacienteAntecedentesUpdateView, self).get_context_data(**kwargs)
        context.update({
            'ultimos_embarazos': self.get_ultimos_embarazos(),
            'paciente': self.paciente,
            'vacuna_form': self.get_vacuna_form()
        })
        return context

    def form_valid(self, form, vacuna_form):
        self.object = form.save()
        vacuna_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, vacuna_form):
        return self.render_to_response(
            self.get_context_data(form=form, vacuna_form=vacuna_form))

    def get_success_url(self):
        messages.success(
            self.request, u'Se actualizaron los antecedentes ginecologicos')
        return reverse(
            'controles:list', kwargs={'paciente_id': self.paciente.id})

    def get_ultimos_embarazos(self):
        return UltimoEmbarazo.objects.filter(
            paciente=self.paciente).order_by('numero')

    def get_vacuna_form(self):
        vacuna, created = Vacuna.objects.get_or_create(paciente=self.paciente)
        form = VacunaPreForm(self.request.POST or None, instance=vacuna)
        return form


class PacienteControlAntecedentesUpdateView(EstablecimientoRequiredMixin, HistoriaClinicaRequiredMixin, UpdateView):
    template_name = 'pacientes/control_antecedentes.html'
    form_class = AntecedenteGinecologicoForm
    paciente = None
    object = None
    permissions = ('pacientes.change_antecedenteginecologico',)

    def dispatch(self, request, *args, **kwargs):
        self.paciente = get_object_or_404(Paciente, id=kwargs.get('id', 0))
        return super(PacienteControlAntecedentesUpdateView, self).dispatch(
            request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(
            self.request.POST, instance=self.get_object())
        vacuna_form = self.get_vacuna_form()
        if form.is_valid() and vacuna_form.is_valid():
            return self.form_valid(form, vacuna_form)
        else:
            return self.form_invalid(form, vacuna_form)

    def get_object(self, queryset=None):
        return self.paciente.antecedente_ginecologico

    def get_context_data(self, **kwargs):
        context = super(
            PacienteControlAntecedentesUpdateView, self).get_context_data(**kwargs)
        context.update({
            'ultimos_embarazos': self.get_ultimos_embarazos(),
            'paciente': self.paciente,
            'vacuna_form': self.get_vacuna_form()
        })
        return context

    def form_valid(self, form, vacuna_form):
        self.object = form.save()
        vacuna_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, vacuna_form):
        return self.render_to_response(
            self.get_context_data(form=form, vacuna_form=vacuna_form))

    def get_success_url(self):
        messages.success(
            self.request, u'Se actualizaron los antecedentes ginecologicos')
        return reverse(
            'embarazos:create-control-embarazo', kwargs={'paciente_id': self.paciente.id})

    def get_ultimos_embarazos(self):
        return UltimoEmbarazo.objects.filter(
            paciente=self.paciente).order_by('numero')

    def get_vacuna_form(self):
        vacuna, _ = Vacuna.objects.get_or_create(paciente=self.paciente)
        form = VacunaPreForm(self.request.POST or None, instance=vacuna)
        return form


class AntecedentesFamiliaresView(
    EstablecimientoRequiredMixin, HistoriaClinicaRequiredMixin,
    DetailView):
    template_name = 'pacientes/antecedentes_familiares_edit.html'
    model = Paciente
    context_object_name = 'paciente'
    pk_url_kwarg = 'id'
    paciente_key = 'id'
    permissions = ('pacientes.change_antecedentefamiliar',)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(AntecedentesFamiliaresView, self).dispatch(
            request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response_data = {
            'status': 'success'
        }
        try:
            data = json.loads(request.body)
            relaciones = RelacionParentesco.objects.all()
            paciente = self.get_object()
            paciente.antecedentes_familiares_niega = data['niega']
            paciente.save()
            if data['niega']:
                paciente.antecedentes_familiares.all().delete()
            else:
                for item in data['antecedentes']:
                    cie = ICD10.objects.get(codigo=item['codigo'])
                    antecedente, created = (
                        AntecedenteFamiliar.objects.get_or_create(
                            cie=cie, paciente=paciente))
                    if item['delete']:
                        antecedente.delete()
                    else:
                        antecedente.observacion = item['observacion']
                        antecedente.save()
                        if not created:
                            antecedente.relaciones.clear()
                        for rel in item['relaciones']:
                            antecedente.relaciones.add(
                                relaciones.get(id=int(rel)))
        except ValueError:
            response_data['status'] = 'error'
        return JsonResponse(response_data)

    def get_context_data(self, **kwargs):
        context = super(
            AntecedentesFamiliaresView, self).get_context_data(**kwargs)
        cies = self.get_cies()
        cies = cies.exclude(codigo__in=[
            af.cie.codigo for af in self.object.antecedentes_familiares.all()])
        context.update({
            'cies': cies.order_by('nombre_mostrar', 'nombre'),
            'relaciones': RelacionParentesco.objects.filter(
                Q(solo_femenino=False) | Q(nombre__icontains='madre')
            ).order_by('nombre'),
            'fem_relaciones': RelacionParentesco.objects.filter(
                Q(solo_femenino=True) | Q(nombre__icontains='Otros')
            ).order_by('nombre'),
            'cies_solo_fem': ICD10.objects.filter(codigo__in=['O16X', 'O308'])
        })
        return context

    def get_cies(self):
        codes = [
            'A150', 'A169', 'B54X', 'I10X', 'O16X', 'O309', 'T784', 'Z809',
            'Z811', 'Z812', 'Z820', 'Z825', 'Z827', 'Z831', 'Z833', 'Z834']
        return ICD10.objects.filter(codigo__in=codes)


class AntecedentesMedicosView(
    EstablecimientoRequiredMixin, HistoriaClinicaRequiredMixin,
    DetailView):
    template_name = 'pacientes/antecedentes_medicos_edit.html'
    model = Paciente
    context_object_name = 'paciente'
    pk_url_kwarg = 'id'
    paciente_key = 'id'
    permissions = ('pacientes.change_antecedentemedico',)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(
            AntecedentesMedicosView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response_data = {
            'status': 'success'
        }
        try:
            data = json.loads(request.body)
            paciente = self.get_object()
            paciente.antecedentes_medicos_niega = data['niega']
            paciente.save()
            if data['niega']:
                paciente.antecedentes_medicos.all().delete()
            else:
                for item in data['antecedentes']:
                    cie = ICD10Medical.objects.get(codigo=item['codigo'])
                    antecedente, created = (
                        AntecedenteMedico.objects.get_or_create(
                            cie=cie, paciente=paciente))
                    if item['delete']:
                        antecedente.delete()
                    else:
                        antecedente.observacion = item['observacion']
                        antecedente.save()
        except ValueError:
            response_data['status'] = 'failed'
        return JsonResponse(response_data)

    def get_context_data(self, **kwargs):
        context = super(
            AntecedentesMedicosView, self).get_context_data(**kwargs)
        cies = self.get_cies()
        cies = cies.exclude(codigo__in=[
            am.cie.codigo for am in self.object.antecedentes_medicos.all()])
        context.update({
            'cies': cies.order_by('nombre_mostrar', 'nombre')
        })
        return context

    def get_cies(self):
        codes = [
            'A153', 'A64X9', 'B24X', 'E149', 'G409', 'I429', 'J459', 'N979',
            'O149', 'O159', 'O16X', 'O601', 'O639', 'O722', 'O730', 'R456',
            'T652', 'Y919', 'Z21X1', 'Z351', 'Z354', 'Z356', 'Z860', 'Z861',
            'Z864', 'Z865', 'Z867', 'Z877', 'Z888', 'Z924']
        return ICD10Medical.objects.filter(codigo__in=codes)


class AntecedentesResumeJsonView(View):
    def get(self, request, *args, **kwargs):
        paciente = self.get_paciente()
        ao = paciente.antecedente_obstetrico
        data = {
            'gestas': ao.gestaciones,
            'abortos': ao.abortos,
            'partos': ao.partos,
            'vaginales': ao.vaginales,
            'cesareas': ao.cesareas,
            'nacidos_vivos': ao.nacidos_vivos,
            'nacidos_muertos': ao.nacidos_muertos,
            'viven': ao.viven,
            'muerto_primera_semana': ao.muertos_menor_una_sem,
            'muerto_despues_primera_semana': ao.muertos_mayor_igual_1sem,
            'cero_o_mas_3': 'X' if ao.gestaciones == 0 or ao.gestaciones > 3 else '',
            'menor_2500_g': 'X' if ao.nacidos_menor_2500g else '',
            'multiple': 'X' if ao.embarazos_multiples else '',
            'menor_37_sem': 'X' if ao.nacidos_menor_37sem else '',
            'mayor_peso': ao.rn_mayor_peso
        }
        return JsonResponse(data)

    def get_paciente(self):
        try:
            paciente = Paciente.objects.get(id=self.kwargs.get('id', 0))
            return paciente
        except Paciente.DoesNotExist:
            raise Http404
