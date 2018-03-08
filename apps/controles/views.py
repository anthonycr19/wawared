# coding: utf-8
import json
import types
import hashlib
from cStringIO import StringIO

from datetime import datetime, timedelta
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import (
    HttpResponseRedirect, Http404, HttpResponse, HttpResponseNotAllowed)
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    DetailView, CreateView, UpdateView, RedirectView, View)
from django.db import IntegrityError

from cie.models import ICD10
from cpt.models import CatalogoProcedimiento
from citas.models import Cita
from common.views import ExcelView
from dashboard.views import EstablecimientoRequiredMixin
from embarazos.models import Embarazo, ganancia_peso_materno_data_segun_imc
from pacientes.models import Paciente, Vacuna
from pacientes.forms import VacunaForm
from popup_messages.models import PopupMessage
from establecimientos.models import Establecimiento
from citas.citasminsa import CitasRest

from . import fuas, reports
from .forms import (
    ControlForm, ExamenFisicoForm, LaboratorioForm, DiagnosticoForm, ExamenFisicoFetalFormSet)
from .models import (
    Control, Sintoma, ExamenFisico, Laboratorio, Diagnostico,
    DiagnosticoDetalle, ProcedimientoDetalle, ExamenFisicoFetal)
from firma.models import Document



class ControlesView(EstablecimientoRequiredMixin, DetailView):
    template_name = 'controles/controles.html'
    model = Paciente
    pk_url_kwarg = 'paciente_id'
    context_object_name = 'paciente'
    embarazo = None
    paciente_key = 'paciente_id'

    def get(self, request, *args, **kwargs):
        paciente = self.get_object()
        try:
            embarazo = Embarazo.objects.get(paciente=paciente, activo=True)
            self.embarazo = embarazo
            return super(ControlesView, self).get(request, *args, **kwargs)
        except Embarazo.DoesNotExist:
            # messages.warning(
            #    request,
            #    u'No existe un embarazo activo, debe crear uno primero')
            return HttpResponseRedirect(reverse(
                'embarazos:create', kwargs={'paciente_id': paciente.id}))

    def get_context_data(self, **kwargs):
        context = super(ControlesView, self).get_context_data(**kwargs)
        paciente = self.get_object()
        identifier_hc = hashlib.md5(b'hc_{}_{}'.format(paciente.id,self.embarazo.id))
        hc_report_sign = False if Document.objects.filter(identifier=identifier_hc.hexdigest()).\
                                      exclude(signed_file='').count() == 0 else True

        identifier_pp = hashlib.md5(b'pp_{}_{}'.format(paciente.id, self.embarazo.id))
        pp_report_sign = False if Document.objects.filter(identifier=identifier_pp.hexdigest()). \
                                      exclude(signed_file='').count() == 0 else True
        context.update({
            'controles': Control.objects.filter(
                embarazo=self.embarazo).order_by('numero'),
            'embarazo': self.embarazo,
            'historia_clinica_sign':hc_report_sign,
            'plan_parto_sign': pp_report_sign,
        })
        return context


def control_next_url(key, control):
    keys = {
        'examen_fisico': reverse(
            'controles:examen_fisico', kwargs={'id': control.id}),
        'laboratorio': reverse(
            'controles:laboratorio', kwargs={'id': control.id}),
        'diagnostico': reverse(
            'controles:diagnostico', kwargs={'id': control.id}),
        'sintomas': reverse('controles:sintomas', kwargs={'id': control.id}),
        'agregar_ecografia': reverse(
            'embarazos:ecografia_create', kwargs={
                'paciente_id': control.paciente.id})
    }
    return keys.get(key, None)


class ControlCreateView(EstablecimientoRequiredMixin, CreateView):
    template_name = 'controles/create.html'
    model = Control
    form_class = ControlForm
    permissions = ('controles.add_control',)
    embarazo = None

    def dispatch(self, request, *args, **kwargs):
        try:
            embarazo = Embarazo.objects.get(id=kwargs.get('embarazo_id', 0))
            self.embarazo = embarazo

            '''
            if self.embarazo.ecografias.all().order_by('fecha').first():
                ecografia = self.embarazo.ecografias.all().order_by('fecha').first()
                if ecografia.fecha_probable_parto is None:
                    messages.warning(request, u'La fecha probable de parto en ecografia no es valida, corregir antes de continuar')
                    return HttpResponseRedirect(reverse('embarazos:ecografia_edit', kwargs={'paciente_id': embarazo.paciente.id , 'id':ecografia.id}))
            '''
            if Control.objects.filter(embarazo=self.embarazo).count() == 15:
                messages.warning(
                    request, u'Se ha agregado la cantidad maxima de controles')
                return HttpResponseRedirect(reverse(
                    'controles:list', kwargs={
                        'paciente_id': embarazo.paciente.id}))
            else:
                last_control = Control.objects.filter(
                    embarazo=embarazo).order_by('numero').last()
                if last_control:
                    if last_control.visito_diagnosticos:
                        return super(ControlCreateView, self).dispatch(
                            request, *args, **kwargs)
                    else:
                        messages.warning(
                            request,
                            u'Primero debe ingresar a '
                            'diagnosticos en el ultimo control para crear '
                            'uno nuevo')
                        return HttpResponseRedirect(reverse(
                            'controles:list', kwargs={
                                'paciente_id': embarazo.paciente.id}))
                else:
                    return super(ControlCreateView, self).dispatch(
                        request, *args, **kwargs)
        except Embarazo.DoesNotExist:
            raise Http404

    def get_form(self, form_class):
        form = super(ControlCreateView, self).get_form(form_class)
        form.set_embarazo(self.embarazo)
        last_control = self.embarazo.controles.order_by('-numero').first()
        if last_control is not None:
            initial_fields_for_copy = (
                'eg_elegida', 'ic_medicina', 'ic_medicina_fecha_1',
                'ic_medicina_fecha_2', 'ic_medicina_fecha_3', 'ic_nutricion',
                'ic_nutricion_fecha_1', 'ic_nutricion_fecha_2',
                'ic_nutricion_fecha_3', 'ic_odontologia',
                'ic_odontologia_fecha_1', 'ic_odontologia_fecha_2',
                'ic_odontologia_fecha_3', 'ic_psicologia',
                'ic_psicologia_fecha_1', 'ic_psicologia_fecha_2',
                'ic_psicologia_fecha_3', 'ic_enfermeria',
                'ic_enfermeria_fecha_1', 'ic_enfermeria_fecha_2',
                'ic_enfermeria_fecha_3', 'ic_laboratorio',
                'ic_laboratorio_fecha_1', 'ic_laboratorio_fecha_2',
                'ic_laboratorio_fecha_3', 'ic_ecografia',
                'ic_ecografia_fecha_1', 'ic_ecografia_fecha_2',
                'ic_ecografia_fecha_3', 'psicoprofilaxis_fecha_1',
                'psicoprofilaxis_fecha_2', 'psicoprofilaxis_fecha_3',
                'psicoprofilaxis_fecha_4', 'psicoprofilaxis_fecha_5',
                'psicoprofilaxis_fecha_6', 'visita_domiciliaria_fecha_1', 'visita_domiciliaria_fecha_2',
                'visita_domiciliaria_fecha_3', 'visita_domiciliaria_fecha_4', 'visita_domiciliaria_fecha_5',
                'visita_domiciliaria_fecha_6', 'visita_domiciliaria_actividad_1', 'visita_domiciliaria_actividad_2',
                'visita_domiciliaria_actividad_3', 'visita_domiciliaria_actividad_4', 'visita_domiciliaria_actividad_5',
                'visita_domiciliaria_actividad_6')
            for initial_field in initial_fields_for_copy:
                form.fields[initial_field].initial = getattr(
                    last_control, initial_field)
        return form

    def get_examen_fisico_fetal_formset(self):
        return ExamenFisicoFetalFormSet(self.request.POST or None, instance=self.object)

    def form_valid(self, form):
        context = self.get_context_data()
        exff_formset = context['exf_formset']
        vacuna_form = self.get_vacuna_form()
        if vacuna_form.is_valid():
            vacuna_form.save()
        if not form.is_valid():
            context = self.get_context_data(form=form)
            context['exf_formset'] = exff_formset
            return self.render_to_response(context)

        control = form.save(commit=False)
        control.embarazo = self.embarazo
        control.paciente = self.embarazo.paciente
        control.establecimiento_id = self.request.session['establecimiento_id']
        control.atencion_hora = datetime.today().time().replace(second=0, microsecond=0)
        control.created_by = self.request.user

        ultimo_control = Control.objects.filter(embarazo=self.embarazo, atencion_fecha=control.atencion_fecha)[:1]
        if ultimo_control and ultimo_control[0].atencion_fecha == control.atencion_fecha:
            messages.warning(self.request, u'Se está intentando agregar un control en el mismo día')
            return HttpResponseRedirect(reverse(
                    'controles:list', kwargs={'paciente_id': control.paciente.id}))

        for i in range(0, len(exff_formset)):
            exff_formset[i].set_control(control)

        if not exff_formset.is_valid():
            context = self.get_context_data(form=form)
            context['exf_formset'] = exff_formset
            return self.render_to_response(context)

        try:
            control.save()
        except IntegrityError:
            control = Control.objects.get(embarazo=control.embarazo, paciente=control.paciente, \
                                          establecimiento_id=control.establecimiento_id, \
                                          atencion_hora=control.atencion_hora, created_by=control.created_by)

        '''
        models = exff_formset.save(commit=False)
        for member in models:
            member.control = control
            member.save()
        '''
        for exf_form in exff_formset:
            if not exf_form.get_eliminado():
                member = exf_form.save(commit=False)
                member.control = control
                member.save()

        establecimiento_actual = Establecimiento.objects.get(id=self.request.session['establecimiento_id'])
        if not establecimiento_actual.is_sistema_externo_admision:
            try:

                if establecimiento_actual.modulo_citas:
                    # enviar confirmacion de cita a citas minsa
                    fecha = control.atencion_fecha.today() + timedelta(days=1)
                    cita = Cita.objects.filter(paciente=self.embarazo.paciente,
                                               establecimiento_id=self.request.session['establecimiento_id'],
                                               fecha__lt=fecha).order_by('-fecha').first()

                    if cita:
                        if cita.uuid_cita_minsa and not cita.is_confirmado_cita_minsa:
                            citas_rest = CitasRest()
                            citas_rest.confirmar_cita(cita.uuid_cita_minsa, 15)
                            cita.is_confirmado_cita_minsa = True
                            cita.save()
                else:
                    Cita.objects.create(
                        establecimiento=establecimiento_actual,
                        paciente=self.embarazo.paciente,
                        asistio=False,
                        control=control,
                        tipo=Cita.TIPO_CONTROL,
                        fecha=datetime.combine(form.cleaned_data['proxima_cita'],
                                               Cita.get_next_available_hour_for_day(
                                                   establecimiento_actual,
                                                   control.proxima_cita)))
                    return super(ControlCreateView, self).form_valid(form)

            except Exception as e:
                print(e)
                '''form.add_error(
                    'proxima_cita',
                    'Ya existe una cita para esta paciente en este dia')
                return super(ControlCreateView, self).form_invalid(form)'''

        return super(ControlCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ControlCreateView, self).get_context_data(**kwargs)
        establecimiento_actual = Establecimiento.objects.get(id=self.request.session['establecimiento_id'])
        try:
            control = Control.objects.get(
                paciente=self.embarazo.paciente.id, numero=1)
            primer_control_presion_diastolica = control.presion_diastolica
            primer_control_presion_sistolica = control.presion_sistolica
        except Exception as e:
            primer_control_presion_diastolica = -1
            primer_control_presion_sistolica = -1

        exf_formset = self.get_examen_fisico_fetal_formset()

        context.update({
            'paciente': self.embarazo.paciente,
            'establecimiento': establecimiento_actual,
            'embarazo': self.embarazo,
            'primer_control_presion_diastolica':
                primer_control_presion_diastolica,
            'primer_control_presion_sistolica':
                primer_control_presion_sistolica,
            'numero_control': Control.objects.filter(
                embarazo=self.embarazo).count() + 1,
            'exf_formset': exf_formset,
            'vacuna_form': self.get_vacuna_form()
        })
        return context

    def get_success_url(self):
        messages.success(self.request, u'Se registro un nuevo control')
        if self.object.calculate_edad_gestacional_semanas() >= 28:
            _message = 'Es necesario que se vuelvan a hacer los siguientes '
            'examenes de laboratorio: hemoglobina, glicemia, examen de orina'
            PopupMessage.register(reverse('controles:diagnostico', kwargs={
                'id': self.object.id}), _message)
        Control.order_by_date(self.embarazo)
        prev_control = self.embarazo.controles.exclude(id=self.object.id).last()
        if prev_control:
            if hasattr(prev_control, 'diagnostico') and prev_control.diagnostico:
                dx = prev_control.diagnostico
                if dx.examenes_pendientes():
                    PopupMessage.register(reverse(
                        'controles:laboratorio', kwargs={'id': self.object.id}),
                        'Hay examenes de laboratorio pendientes por registrar')
                    return reverse('controles:laboratorio', kwargs={'id': self.object.id})
        next_url_param = self.request.POST.get('next_url', None)

        self._update_cita(self.object)
        if next_url_param:
            next_url = control_next_url(next_url_param, self.object)
            if next_url.__len__() > 0:
                return next_url
        return reverse('controles:sintomas', kwargs={'id': self.object.id})

    def get_form_kwargs(self):
        kwargs = super(ControlCreateView, self).get_form_kwargs()
        kwargs.update({'establecimiento_id': self.request.session['establecimiento_id']})
        return kwargs

    def _update_cita(self, control):
        establecimiento_actual = Establecimiento.objects.get(id=self.request.session['establecimiento_id'])
        fecha = control.atencion_fecha.today() + timedelta(days=1)

        if not establecimiento_actual.is_sistema_externo_admision:

            cita = Cita.objects.filter(paciente=self.embarazo.paciente,
                                       establecimiento_id=self.request.session['establecimiento_id'], asistio=False,
                                       fecha__lt=fecha).order_by(
                '-fecha').first()
        else:
            cita = Cita.objects.filter(paciente=self.embarazo.paciente,
                                       establecimiento_id=self.request.session['establecimiento_id'], asistio=False,
                                       fecha__lt=fecha, especialista=self.request.user).order_by(
                '-fecha').first()

        if cita is not None:
            cita.fecha_asistio = datetime.combine(
                control.atencion_fecha,
                control.atencion_hora)
            cita.control = control
            cita.asistio = True
            cita.save()
            messages.success(
                self.request, 'Cita del dia {} actualizada'.format(
                    cita.fecha.strftime('%d-%m-%Y')))

    def get_vacuna_form(self):
        vacuna, created = Vacuna.objects.get_or_create(paciente=self.embarazo.paciente)
        form = VacunaForm(self.request.POST or None, instance=vacuna)
        return form


class ControlDetailView(EstablecimientoRequiredMixin, UpdateView):
    template_name = 'controles/edit.html'
    model = Control
    form_class = ControlForm
    pk_url_kwarg = 'id'
    context_object_name = 'control'

    def post(self, request, *args, **kwargs):
        return HttpResponseNotAllowed('')

    def get_form_kwargs(self):
        kwargs = super(ControlDetailView, self).get_form_kwargs()
        kwargs.update({'establecimiento_id': self.request.session['establecimiento_id']})
        return kwargs

    def get_vacuna_form(self):
        vacuna, created = Vacuna.objects.get_or_create(paciente=self.object.embarazo.paciente)
        form = VacunaForm(self.request.POST or None, instance=vacuna)
        return form

    def get_context_data(self, **kwargs):
        context = super(ControlDetailView, self).get_context_data(**kwargs)
        context.update({
            'paciente': self.object.paciente,
            'embarazo': self.object.embarazo,
            'vacuna_form': self.get_vacuna_form()
        })
        return context


class ControlUpdateView(EstablecimientoRequiredMixin, UpdateView):
    template_name = 'controles/edit.html'
    model = Control
    form_class = ControlForm
    pk_url_kwarg = 'id'
    context_object_name = 'control'
    permissions = ('controles.change_control',)

    def form_valid(self, form):
        context = self.get_context_data()
        exff_formset = context['exf_formset']
        vacuna_form = self.get_vacuna_form()
        if vacuna_form.is_valid():
            vacuna_form.save()
        if exff_formset.is_valid():
            for exf_form in exff_formset:
                if exf_form.get_eliminado():
                    if exf_form.instance.id:
                        exf_form.instance.delete()
                else:
                    exf_form.save()

        else:
            return super(ControlUpdateView, self).form_invalid(form)

        return super(ControlUpdateView, self).form_valid(form)

    def get_examen_fisico_fetal_formset(self):
        return ExamenFisicoFetalFormSet(self.request.POST or None, instance=self.object)

    def get_context_data(self, **kwargs):
        context = super(ControlUpdateView, self).get_context_data(**kwargs)
        establecimiento_actual = Establecimiento.objects.get(id=self.request.session['establecimiento_id'])
        try:
            control = Control.objects.get(
                paciente=self.object.paciente.id, numero=1)
            primer_control_presion_diastolica = control.presion_diastolica
            primer_control_presion_sistolica = control.presion_sistolica

        except Exception as e:
            primer_control_presion_diastolica = -1
            primer_control_presion_sistolica = -1

        if self.object:
            examenesFisicosFet = ExamenFisicoFetal.objects.filter(control=self.object)

            if len(examenesFisicosFet) == 0:
                examFisFet = ExamenFisicoFetal()
                examFisFet.control = self.object
                examFisFet.fcf = self.object.fcf
                examFisFet.situacion = self.object.situacion
                examFisFet.presentacion = self.object.presentacion
                examFisFet.posicion = self.object.posicion
                examFisFet.movimientos_fetales = self.object.movimientos_fetales
                examFisFet.created = self.object.created

                examFisFet.save()

        exf_formset = self.get_examen_fisico_fetal_formset()

        identifier_pp = hashlib.md5(b'pp_{}'.format(self.object.embarazo.id))
        pp_report_sign = False if Document.objects.filter(identifier=identifier_pp.hexdigest()). \
                                      exclude(signed_file='').count() == 0 else True

        identifier_tv = hashlib.md5(b'tv_{}'.format(self.object.embarazo.id))
        tv_report_sign = False if Document.objects.filter(identifier=identifier_tv.hexdigest()). \
                                      exclude(signed_file='').count() == 0 else True

        identifier_cp = hashlib.md5(b'cp_{}'.format(self.object.id))
        cp_report_sign = False if Document.objects.filter(identifier=identifier_cp.hexdigest()). \
                                      exclude(signed_file='').count() == 0 else True

        context.update({
            'paciente': self.object.paciente,
            'establecimiento': establecimiento_actual,
            'embarazo': self.object.embarazo,
            'primer_control_presion_diastolica':primer_control_presion_diastolica,
            'primer_control_presion_sistolica':primer_control_presion_sistolica,
            'exf_formset': exf_formset,
            'tamizaje_violencia_sign':tv_report_sign,
            'control_prenatal_sign': cp_report_sign,
            'plan_parto_sign': pp_report_sign,
            'vacuna_form': self.get_vacuna_form()
        })

        return context

    def get_form_kwargs(self):
        kwargs = super(ControlUpdateView, self).get_form_kwargs()
        kwargs.update({'establecimiento_id': self.request.session['establecimiento_id']})
        return kwargs

    def get_success_url(self):
        messages.success(self.request, u'Control actualizado')
        Control.order_by_date(self.object.embarazo)
        next_url_param = self.request.POST.get('next_url', None)
        if next_url_param:
            next_url = control_next_url(next_url_param, self.object)
            if next_url:
                return next_url
        return reverse('controles:sintomas', kwargs={'id': self.object.id})

    def get_vacuna_form(self):
        vacuna, created = Vacuna.objects.get_or_create(paciente=self.object.embarazo.paciente)
        form = VacunaForm(self.request.POST or None, instance=vacuna)
        return form


class ControlDeleteView(EstablecimientoRequiredMixin, RedirectView):
    permanent = False
    permissions = ('controles.delete_control',)

    def get_redirect_url(self, *args, **kwargs):
        control = get_object_or_404(Control, id=kwargs.get('id', 0))
        paciente_id = control.paciente.id
        control.delete()
        messages.success(self.request, u'Control eliminado')
        return reverse('controles:list', kwargs={'paciente_id': paciente_id})


class SintomasDetailView(EstablecimientoRequiredMixin, DetailView):
    model = Control
    template_name = 'controles/sintomas.html'
    context_object_name = 'control'
    pk_url_kwarg = 'id'

    def post(self, request, *args, **kwargs):
        return HttpResponseNotAllowed('')

    def get_context_data(self, **kwargs):
        context = super(SintomasDetailView, self).get_context_data(**kwargs)
        sintomas = Sintoma.objects.filter(control=self.object)
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
            'N939', 'O419', 'O363', 'O624', 'R104', 'R398', 'R101', 'R11X',
            'R418', 'R51X', 'R509', 'R568', 'H931', 'H579']

        return ICD10.objects.filter(codigo__in=codes)


class SintomasView(EstablecimientoRequiredMixin, DetailView):
    model = Control
    template_name = 'controles/sintomas.html'
    context_object_name = 'control'
    pk_url_kwarg = 'id'
    permissions = ('controles.change_sintoma',)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        control = self.get_object()
        if not control.visito_sintomas:
            control.visito_sintomas = True
            control.save()
        return super(SintomasView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            data = json.loads(request.body)
            control = self.get_object()

            control.asintomatica = data['asintomatica']

            control.save()

            if data['asintomatica']:
                control.sintomas.all().delete()
            else:
                for item in data['sintomas']:
                    cie = ICD10.objects.get(codigo=item['codigo'])
                    try:
                        sintoma = Sintoma.objects.get(cie=cie, control=control)
                    except Sintoma.DoesNotExist:
                        sintoma = Sintoma.objects.create(
                            cie=cie, control=control, created_by=request.user)
                    if item['delete']:
                        sintoma.delete()
                    else:
                        sintoma.observacion = item['observacion']
                        sintoma.save()
                messages.success(request, u'Sintomas guardados')
            return JsonResponse({
                'url': reverse('controles:sintomas', kwargs={'id': control.id})
            })
        else:
            control = self.get_object()
            next_url = request.POST['next_url']
            if next_url:
                if next_url == 'agregar_ecografia':

                    return HttpResponseRedirect(
                        reverse('embarazos:ecografia_create', kwargs={'paciente_id': control.paciente.id}))
                else:
                    return HttpResponseRedirect(reverse('controles:{}'.format(next_url), kwargs={'id': control.id}))

    def get_context_data(self, **kwargs):
        context = super(SintomasView, self).get_context_data(**kwargs)
        sintomas = Sintoma.objects.filter(control=self.object)
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


class ExamenFisicoView(EstablecimientoRequiredMixin, UpdateView):
    template_name = 'controles/examen_fisico.html'
    model = ExamenFisico
    form_class = ExamenFisicoForm
    context_object_name = 'examen_fisico'
    control = None
    permissions = ('controles.change_examenfisico',)

    def dispatch(self, request, *args, **kwargs):
        self.control = self.get_control(**kwargs)
        return super(ExamenFisicoView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            obj = self.model.objects.get(control=self.control)
        except ExamenFisico.DoesNotExist:
            obj = self.model.objects.create(
                control=self.control, created_by=self.request.user)
        return obj

    def get_context_data(self, **kwargs):
        context = super(ExamenFisicoView, self).get_context_data(**kwargs)
        context.update({
            'control': self.control,
            'paciente': self.control.paciente
        })
        return context

    def form_valid(self, form):
        ef = form.save(commit=False)
        if ef.nivel_conciencia != ExamenFisico.NIVEL_CONCIENCIA_OTROS:
            ef.nivel_conciencia_otros = ''
        ef.save()
        return super(ExamenFisicoView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, u'Examen fisico guardado')

        next_url = self.request.POST.get('next_url')

        if next_url:
            if next_url == 'agregar_ecografia':
                return reverse('embarazos:ecografia_create', kwargs={'paciente_id': self.control.paciente.id})
            else:
                return reverse('controles:{}'.format(next_url), kwargs={'id': self.control.id})

        return reverse('controles:laboratorio', kwargs={'id': self.control.id})

    def get_control(self, **kwargs):
        try:
            control = Control.objects.get(id=kwargs.get('id', 0))
            return control
        except Control.DoesNotExist:
            raise Http404


class ExamenFisicoDetailView(ExamenFisicoView):
    permissions = ()

    def post(self, request, *args, **kwargs):
        return HttpResponseNotAllowed('')


# Nueva view de test para probar el nuevo modelo de datos.
class LaboratorioView(EstablecimientoRequiredMixin, UpdateView):
    template_name = 'controles/laboratorio.html'
    model = Laboratorio
    form_class = LaboratorioForm
    context_object_name = 'laboratorio'
    paciente = None  # referencias a las llaves.
    embarazo = None  # referencias a las llaves.
    control = None  # esta es una referencia temporal.

    permissions = ('controles.change_laboratorio',)

    def dispatch(self, request, *args, **kwargs):
        self.paciente = self.get_paciente(**kwargs)
        try:
            embarazo = Embarazo.objects.get(paciente=self.paciente, activo=True)
            self.embarazo = embarazo
            return super(LaboratorioView, self).dispatch(request, *args, **kwargs)
        except Embarazo.DoesNotExist:
            messages.warning(
                request,
                u'No existe un embarazo activo, debe crear uno primero')
            return HttpResponseRedirect(
                reverse('embarazos:create', kwargs={'id': self.paciente.id}))

    def get_object(self, queryset=None):

        if not hasattr(self, 'object'):
            try:
                self.object = self.model.objects.get(paciente=self.paciente, embarazo=self.embarazo)
                self.object.control = self.control
            except Laboratorio.DoesNotExist:
                last_control = Control.objects.filter(paciente=self.paciente, embarazo=self.embarazo).last()
                if hasattr(last_control, 'laboratorio'):
                    self.object = last_control.laboratorio
                    self.object.paciente = self.paciente
                    self.object.embarazo = self.embarazo
                    self.object.save()
                else:
                    self.object = self.model.objects.create(paciente=self.paciente, embarazo=self.embarazo,
                                                            created_by=self.request.user)

        return self.object

    def get_context_data(self, **kwargs):
        context = super(LaboratorioView, self).get_context_data(**kwargs)
        context.update({
            'paciente': self.paciente,
            'embarazo': self.embarazo,
            'control': self.control
        })
        return context

    def get_success_url(self):
        messages.success(self.request, u'Laboratorio actualizado')
        next_url = self.request.POST.get('next_url')

        if next_url:
            if next_url == 'agregar_ecografia':
                return reverse('embarazos:ecografia_create', kwargs={'paciente_id': self.object.paciente.id})
            else:
                return reverse('controles:{}'.format(next_url), kwargs={'id': self.control.id})

        # return reverse('controles:list', kwargs={'paciente_id': self.paciente.id})
        return reverse('controles:diagnostico', kwargs={'id': self.control.id})

    def get_paciente(self, **kwargs):
        # Con la finalidad de no cambiar la arquitectura de las rutas actuales en wawared
        # estoy usando el control para recuperar el paciente.
        try:
            self.control = Control.objects.get(id=kwargs.get('id', 0))
            paciente = self.control.paciente
            return paciente
        except Control.DoesNotExist:
            raise Http404


class LaboratorioDetailView(LaboratorioView):
    permissions = ()

    def post(self, request, *args, **kwargs):
        return HttpResponseNotAllowed('')


class DiagnosticoView(EstablecimientoRequiredMixin, UpdateView):
    model = Diagnostico
    template_name = 'controles/diagnostico.html'
    context_object_name = 'diagnostico'
    form_class = DiagnosticoForm
    control = None
    object = None
    permissions = ('controles.change_diagnostico',)
    puntaje_cie = None

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        self.control = self.get_control(**kwargs)
        if not self.control.visito_diagnosticos:
            self.control.visito_diagnosticos = True
            self.control.save()
        try:
            diagnostico = self.model.objects.get(control=self.control)
        except Diagnostico.DoesNotExist:
            diagnostico = self.model.objects.create(
                control=self.control,
                created_by=request.user,
                paciente=self.control.paciente,
                proxima_cita=self.control.proxima_cita,
                tratamiento='\n'.join(self.control.generar_tratamiento())
            )
        self.object = diagnostico
        return super(DiagnosticoView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            try:
                data = json.loads(request.body)

                for item in data["cie"]:
                    cie = ICD10.objects.get(codigo=item['codigo'])

                    detalle = DiagnosticoDetalle.objects.filter(cie=cie, diagnostico=self.object).first()

                    if not detalle:
                        detalle = DiagnosticoDetalle.objects.create(cie=cie, diagnostico=self.object,
                                                                    created_by=request.user, order=0)

                    if item['delete']:
                        detalle.delete()
                    else:
                        detalle.observacion = item['observacion']
                        detalle.order = item.get('order', 0)
                        detalle.tipo = item['tipo'].upper()
                        detalle.laboratorio = item['laboratorio']
                        detalle.save()

                for item in data["cpt"]:
                    cpt = CatalogoProcedimiento.objects.get(codigo_cpt=item['codigo'])
                    try:
                        procedimiento = ProcedimientoDetalle.objects.get(cpt=cpt, diagnostico=self.object)
                    except ProcedimientoDetalle.DoesNotExist:
                        procedimiento = ProcedimientoDetalle.objects.create(cpt=cpt, diagnostico=self.object,
                                                                            created_by=request.user, order=0)
                    if item['delete']:
                        procedimiento.delete()
                    else:
                        procedimiento.observacion = item['observacion']
                        procedimiento.order = item.get('order', 0)
                        procedimiento.save()

                response_data = {'status': 'success'}
            except ValueError:
                response_data = {'status': 'failed'}

            return JsonResponse(response_data)
        else:
            return super(DiagnosticoView, self).post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.object

    def form_valid(self, form):

        diagnostico = form.save(commit=False)
        diagnostico.paciente = self.control.paciente
        diagnostico.control = self.control
        diagnostico.save()
        if not type(diagnostico.proxima_cita) is types.NoneType:
            self.control.proxima_cita = diagnostico.proxima_cita

        self.control.eg_elegida = self.request.POST['eg_elegida']
        self.control.save()
        return super(DiagnosticoView, self).form_valid(form)

    def get_context_data(self, **kwargs):

        context = super(DiagnosticoView, self).get_context_data(**kwargs)
        detalles = self.object.detalles.all()
        procedimientos = self.object.procedimientos.all()

        if hasattr(self.object.control.embarazo, 'ficha_problema'):
            self.puntaje_cie = (
                self.object.control.embarazo.ficha_problema.get_puntaje_cie())

        cies = self.get_cies()
        cies = cies.exclude(
            id__in=[detalle.cie.id for detalle in detalles]).order_by('nombre')

        try:

            first_cie = cies.get(codigo='Z349')
            cies = cies.exclude(codigo='Z349')
            _cies = [first_cie]
            for cie in cies:
                _cies.append({
                    'id': cie.id,
                    'nombre': cie.nombre,
                    'nombre_mostrar': cie.nombre_mostrar,
                    'codigo': cie.codigo,
                    'nombre_display': cie.nombre_display
                })
            cies = _cies

        except ICD10.DoesNotExist:
            pass

        context.update({
            'paciente': self.control.paciente,
            'control': self.control,
            'cies': cies,
            'detalles': detalles,
            'procedimientos': procedimientos,
            'ficha_puntaje_cie': self.puntaje_cie
        })

        return context

    def get_success_url(self):
        messages.success(self.request, u'Diagnostico actualizado')

        next_url = self.request.POST.get('next_url')

        if next_url:
            if next_url == 'agregar_ecografia':
                return reverse('embarazos:ecografia_create', kwargs={'paciente_id': self.control.paciente.id})
            else:
                return reverse('controles:{}'.format(next_url), kwargs={'id': self.control.id})

        return reverse('controles:list', kwargs={
            'paciente_id': self.control.paciente.id})

    def get_control(self, **kwargs):
        try:
            control = Control.objects.get(id=kwargs.get('id', 0))
            return control
        except Control.DoesNotExist:
            raise Http404

    def get_form_kwargs(self):
        kwargs = super(DiagnosticoView, self).get_form_kwargs()
        kwargs.update({'establecimiento_id': self.request.session['establecimiento_id']})
        return kwargs

    def get_cies(self):
        codes = [
            'O200', 'O219', 'O23', 'Z359', 'Z349', 'N760', 'N952', 'O100',
            'O120', 'Z392', 'O10', 'O44', 'O45', 'O60', 'O46', 'O42', 'O04',
            'Z7171', '86703', 'Z7173', '99403', 'U1692', 'U140', '88141',
            'Z0143', 'U06.9']
        if self.puntaje_cie is not None:
            codes.append(self.puntaje_cie)
        return ICD10.objects.filter(codigo__in=codes)


class DiagnosticoDetailView(DiagnosticoView):
    permissions = ()

    def post(self, request, *args, **kwargs):
        return HttpResponseNotAllowed('')


class DataCrecimientoNeonatalView(View):
    def get(self, request, *args, **kwargs):
        control = Control.objects.get(id=self.kwargs['id'])
        embarazo = control.embarazo
        peso_base = control.embarazo.peso

        controles_values = []
        for control in embarazo.controles.all().order_by('numero'):
            if int(control.edad_gestacional_semanas) >= 13:
                diff = int((control.peso - peso_base) * 1000)
                controles_values.append((
                    control.edad_gestacional_semanas, diff))

        crecimiento_fetal_percentiles = [
            {'10': 690, '50': 820, '5': 660, 'semana': 24, '90': 975,
             '2.5': 630},
            {'10': 690, '50': 840, '5': 650, 'semana': 25, '90': 1055,
             '2.5': 630},
            {'10': 710, '50': 900, '5': 670, 'semana': 26, '90': 1170,
             '2.5': 655},
            {'10': 770, '50': 1005, '5': 730, 'semana': 27, '90': 1315,
             '2.5': 710},
            {'10': 860, '50': 1140, '5': 815, 'semana': 28, '90': 1490,
             '2.5': 790},
            {'10': 980, '50': 1300, '5': 925, 'semana': 29, '90': 1685,
             '2.5': 895},
            {'10': 1125, '50': 1485, '5': 1060, 'semana': 30, '90': 1900,
             '2.5': 1015},
            {'10': 1295, '50': 1690, '5': 1215, 'semana': 31, '90': 2125,
             '2.5': 1150},
            {'10': 1475, '50': 1905, '5': 1380, 'semana': 32, '90': 2360,
             '2.5': 1305},
            {'10': 1665, '50': 2125, '5': 1555, 'semana': 33, '90': 2600,
             '2.5': 1465},
            {'10': 1860, '50': 2345, '5': 1735, 'semana': 34, '90': 2835,
             '2.5': 1630},
            {'10': 2060, '50': 2565, '5': 1920, 'semana': 35, '90': 3060,
             '2.5': 1800},
            {'10': 2250, '50': 2770, '5': 2100, 'semana': 36, '90': 3280,
             '2.5': 1965},
            {'10': 2435, '50': 2960, '5': 2270, 'semana': 37, '90': 3480,
             '2.5': 2135},
            {'10': 2600, '50': 3130, '5': 2435, 'semana': 38, '90': 3655,
             '2.5': 2290},
            {'10': 2750, '50': 3275, '5': 2580, 'semana': 39, '90': 3810,
             '2.5': 2440},
            {'10': 2875, '50': 3385, '5': 2710, 'semana': 40, '90': 3930,
             '2.5': 2580},
            {'10': 2970, '50': 3460, '5': 2815, 'semana': 41, '90': 4020,
             '2.5': 2700},
            {'10': 3030, '50': 3495, '5': 2895, 'semana': 42, '90': 4065,
             '2.5': 2800},
            {'10': 3050, '50': 3480, '5': 2945, 'semana': 43, '90': 4065,
             '2.5': 2875}]

        percentil_2_5 = []
        percentil_5 = []
        percentil_10 = []
        percentil_50 = []
        percentil_90 = []
        for percentil in crecimiento_fetal_percentiles:
            percentil_2_5.append(
                (percentil['semana'], percentil['2.5'])
            )
            percentil_5.append(
                (percentil['semana'], percentil['5'])
            )
            percentil_10.append(
                (percentil['semana'], percentil['10'])
            )
            percentil_50.append(
                (percentil['semana'], percentil['50'])
            )
            percentil_90.append(
                (percentil['semana'], percentil['90'])
            )
        data = [
            {
                'key': 'Percentil 2.5',
                'values': percentil_2_5
            },
            {
                'key': 'Percentil 5',
                'values': percentil_5
            },
            {
                'key': 'Percentil 10',
                'values': percentil_10
            },
            {
                'key': 'Percentil 50',
                'values': percentil_50
            },
            {
                'key': 'Percentil 90',
                'values': percentil_90
            }
        ]
        if controles_values:
            data.append({
                'key': 'Controles',
                'values': controles_values
            })
        return HttpResponse(json.dumps(data), content_type='application/json')


class DataGananciaPesoMaternoView(View):
    def get(self, request, *args, **kwargs):
        control = Control.objects.get(id=self.kwargs['id'])

        embarazo = control.embarazo

        controles_values = []

        peso_base = control.embarazo.peso

        for control in embarazo.controles.all().order_by('numero'):
            if int(control.edad_gestacional_semanas) >= 13:
                diff = float((control.peso - peso_base))
                controles_values.append((
                    control.edad_gestacional_semanas, diff))
        percentiles = [
            {'25': 0.4, '90': 3.5, 'semana': '13'},
            {'25': 1.2, '90': 4.8, 'semana': '14'},
            {'25': 1.3, '90': 4.9, 'semana': '15'},
            {'25': 1.8, '90': 5.1, 'semana': '16'},
            {'25': 2.4, '90': 6.4, 'semana': '17'},
            {'25': 2.6, '90': 7.0, 'semana': '18'},
            {'25': 2.9, '90': 8.1, 'semana': '19'},
            {'25': 3.2, '90': 8.2, 'semana': '20'},
            {'25': 4.1, '90': 8.6, 'semana': '21'},
            {'25': 4.4, '90': 9.2, 'semana': '22'},
            {'25': 4.7, '90': 10.5, 'semana': '23'},
            {'25': 5.1, '90': 10.8, 'semana': '24'},
            {'25': 5.6, '90': 11.3, 'semana': '25'},
            {'25': 5.9, '90': 11.6, 'semana': '26'},
            {'25': 6.0, '90': 11.7, 'semana': '27'},
            {'25': 6.2, '90': 11.9, 'semana': '28'},
            {'25': 6.9, '90': 12.7, 'semana': '29'},
            {'25': 7.7, '90': 13.5, 'semana': '30'},
            {'25': 7.6, '90': 13.9, 'semana': '31'},
            {'25': 7.9, '90': 14.5, 'semana': '32'},
            {'25': 8.1, '90': 14.7, 'semana': '33'},
            {'25': 8.2, '90': 15.0, 'semana': '34'},
            {'25': 8.2, '90': 15.4, 'semana': '35'},
            {'25': 8.2, '90': 15.7, 'semana': '36'},
            {'25': 8.2, '90': 15.7, 'semana': '37'},
            {'25': 8.2, '90': 15.9, 'semana': '38'},
            {'25': 8.2, '90': 16.0, 'semana': '39'},
            {'25': 8.2, '90': 16.0, 'semana': '40'}]

        percentil_25 = []
        percentil_90 = []

        if ExamenFisicoFetal.objects.filter(control=control).count() > 1:
            multiple = True
        else:
            multiple = False

        valores = ganancia_peso_materno_data_segun_imc(control.imc, multiple=multiple)

        for valor in valores:
            percentil_25.append(
                (valor['semana'], valor['min'])
            )
            percentil_90.append(
                (valor['semana'], valor['max'])
            )

        data = [
            {
                'key': 'Percentil 25',
                'values': percentil_25
            },
            {
                'key': 'Percentil 90',
                'values': percentil_90
            }
        ]
        if controles_values:
            data.append({
                'key': 'Controles',
                'values': controles_values
            })
        return HttpResponse(json.dumps(data), content_type='application/json')


class DataAlturaUterinaView(View):
    def get(self, request, *args, **kwargs):
        control = Control.objects.get(id=self.kwargs['id'])

        embarazo = control.embarazo

        controles_values = []
        for control in embarazo.controles.all().order_by('numero'):
            if int(control.edad_gestacional_semanas) >= 13 and control.altura_uterina:
                controles_values.append((
                    control.edad_gestacional_semanas, int(
                        control.altura_uterina)))
        altura_uterina_percentiles = [
            {'10': 8.0, '15': 8.0, '50': 10.8, '75': 11.0, 'semana': 13,
             '90': 12.0},
            {'10': 8.5, '15': 10.0, '50': 11.0, '75': 13.0, 'semana': 14,
             '90': 14.5},
            {'10': 9.5, '15': 10.5, '50': 12.5, '75': 14.0, 'semana': 15,
             '90': 15.0},
            {'10': 11.5, '15': 12.5, '50': 14.0, '75': 16.0, 'semana': 16,
             '90': 18.0},
            {'10': 12.5, '15': 13.0, '50': 15.0, '75': 17.5, 'semana': 17,
             '90': 18.0},
            {'10': 13.5, '15': 15.0, '50': 16.5, '75': 18.0, 'semana': 18,
             '90': 19.0},
            {'10': 14.0, '15': 16.0, '50': 17.5, '75': 19.0, 'semana': 19,
             '90': 19.5},
            {'10': 15.0, '15': 17.0, '50': 18.0, '75': 19.5, 'semana': 20,
             '90': 21.0},
            {'10': 15.5, '15': 18.5, '50': 19.0, '75': 20.0, 'semana': 21,
             '90': 21.5},
            {'10': 16.5, '15': 18.5, '50': 20.0, '75': 21.5, 'semana': 22,
             '90': 22.5},
            {'10': 17.5, '15': 19.5, '50': 21.0, '75': 22.5, 'semana': 23,
             '90': 23.0},
            {'10': 18.5, '15': 20.5, '50': 22.0, '75': 23.0, 'semana': 24,
             '90': 24.0},
            {'10': 19.5, '15': 21.0, '50': 22.5, '75': 24.0, 'semana': 25,
             '90': 25.5},
            {'10': 20.0, '15': 21.5, '50': 23.0, '75': 24.5, 'semana': 26,
             '90': 25.5},
            {'10': 20.5, '15': 21.5, '50': 23.5, '75': 25.0, 'semana': 27,
             '90': 26.5},
            {'10': 21.0, '15': 23.0, '50': 25.0, '75': 26.0, 'semana': 28,
             '90': 27.0},
            {'10': 22.4, '15': 24.0, '50': 25.5, '75': 26.5, 'semana': 29,
             '90': 28.0},
            {'10': 23.5, '15': 24.5, '50': 26.5, '75': 28.0, 'semana': 30,
             '90': 29.0},
            {'10': 24.0, '15': 26.0, '50': 27.0, '75': 28.0, 'semana': 31,
             '90': 29.5},
            {'10': 25.0, '15': 26.5, '50': 28.0, '75': 29.5, 'semana': 32,
             '90': 30.0},
            {'10': 25.5, '15': 26.5, '50': 29.0, '75': 30.0, 'semana': 33,
             '90': 31.0},
            {'10': 26.0, '15': 27.5, '50': 29.5, '75': 31.0, 'semana': 34,
             '90': 32.0},
            {'10': 26.5, '15': 28.5, '50': 30.5, '75': 32.0, 'semana': 35,
             '90': 33.0},
            {'10': 28.0, '15': 29.0, '50': 31.0, '75': 32.5, 'semana': 36,
             '90': 33.0},
            {'10': 28.5, '15': 29.5, '50': 31.5, '75': 33.0, 'semana': 37,
             '90': 34.0},
            {'10': 29.5, '15': 30.5, '50': 33.0, '75': 33.5, 'semana': 38,
             '90': 34.0},
            {'10': 30.5, '15': 31.0, '50': 33.5, '75': 33.5, 'semana': 39,
             '90': 34.0},
            {'10': 31.0, '15': 31.0, '50': 33.5, '75': 33.5, 'semana': 40,
             '90': 34.5}]

        percentil_10 = []
        percentil_90 = []
        for percentil in altura_uterina_percentiles:
            percentil_10.append(
                (percentil['semana'], percentil['10'])
            )
            percentil_90.append(
                (percentil['semana'], percentil['90'])
            )
        data = [
            {
                'key': 'Percentil 10',
                'values': percentil_10
            },
            {
                'key': 'Percentil 90',
                'values': percentil_90
            }
        ]
        if controles_values:
            data.append({
                'key': 'Controles',
                'values': controles_values
            })
        return HttpResponse(json.dumps(data), content_type='application/json')


class SolicitudExamenesClinicosReportView(View):
    def get(self, request, *args, **kwargs):
        control = get_object_or_404(Control, id=kwargs.get('control_id', ''))
        report = reports.SolicitudExamenesClinicosReport(control)
        return report.render_to_response()


class HistoriaClinicaReportView(View):
    def get(self, request, *args, **kwargs):
        accion = kwargs.get('accion_id', None)
        control = get_object_or_404(Control, id=kwargs.get('control_id', ''))
        control.embarazo.create_incremento_peso_materno_chart()
        control.embarazo.create_altura_uterina_chart()
        report = reports.HistoriaClinicaReport(control)
        identifier = hashlib.md5(b'hc_{}_{}'.format(control.paciente.id, control.embarazo.id))
        if accion == '1':
            return report.signed_report(identifier.hexdigest(), request.META.get('HTTP_REFERER', '/'))
        elif accion == "2":
            return report.render_signed_file(identifier.hexdigest())
        else:
            return report.render_to_response()


class PlanPartoReportView(View):
    def get(self, request, *args, **kwargs):
        accion = kwargs.get('accion_id', None)
        control = get_object_or_404(Control, id=kwargs.get('control_id', ''))
        report = reports.PlanPartoReport(control)
        identifier = hashlib.md5(b'pp_{}_{}'.format(control.paciente.id, control.embarazo.id))
        if accion == '1':
            return report.signed_report(identifier.hexdigest(), request.META.get('HTTP_REFERER', '/'))
        elif accion == "2":
            return report.render_signed_file(identifier.hexdigest())
        else:
            return report.render_to_response()


class TarjetaSeguimientoReportView(View):
    def get(self, request, *args, **kwargs):
        control = get_object_or_404(Control, id=kwargs.get('control_id', ''))
        report = reports.TarjetaSeguimientoReport(control)
        return report.render_to_response()


class RecetaUnicaEstandarizadaReportView(View):
    def get(self, request, *args, **kwargs):
        control = get_object_or_404(Control, id=kwargs.get('control_id', ''))
        report = reports.RecetaUnicaEstandarizadaReport(control)
        return report.render_to_response()


class RecetaUnicaFlujoVaginalReportView(View):
    def get(self, request, *args, **kwargs):
        control = get_object_or_404(Control, id=kwargs.get('control_id', ''))
        report = reports.RecetaUnicaFlujoVaginalReport(control)
        return report.render_to_response()


class RecetaUnicaPruebaRapidaReportView(View):
    def get(self, request, *args, **kwargs):
        control = get_object_or_404(Control, id=kwargs.get('control_id', ''))
        report = reports.RecetaUnicaPruebaRapidaReport(control)
        return report.render_to_response()


class FormatoUnicoAtencionReportView(View):
    def get(self, request, *args, **kwargs):
        control = get_object_or_404(Control, id=kwargs.get('control_id', ''))
        report = reports.FormatoUnicoAtencionReport(control)
        return report.render_to_response()


class HojaReferenciaReportView(View):
    def get(self, request, *args, **kwargs):
        control = get_object_or_404(Control, id=kwargs.get('control_id', ''))
        report = reports.HojaReferenciaReport(control)
        return report.render_to_response()


class CarneControlPrenatalReportView(View):
    def get(self, request, *args, **kwargs):
        control = get_object_or_404(Control, id=kwargs.get('control_id', ''))
        control.embarazo.create_incremento_peso_materno_chart()
        control.embarazo.create_altura_uterina_chart()
        report = reports.CarneControlPrenatalReport(control)
        return report.render_to_response()


class SolicitudExamenCitologicoReportView(EstablecimientoRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        control = get_object_or_404(Control, id=kwargs.get('control_id', ''))
        report = reports.SolicitudExamenCitologicoReport(control)
        return report.render_to_response()


class SolicitudPruebaElisaReportView(EstablecimientoRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        control = get_object_or_404(Control, id=kwargs.get('control_id'))
        report = reports.SolicitudPruebaElisaReport(
            control, request.session['establecimiento_id'])
        return report.render_to_response()


class ControlPrenatalExcelReportView(EstablecimientoRequiredMixin, ExcelView):
    filename = 'Control_Prenatal_{}.xlsx'
    control = None

    def dispatch(self, request, *args, **kwargs):
        self.control = get_object_or_404(Control, id=kwargs.get('control_id'))
        self.filename = self.filename.format(self.control.paciente.numero_documento)
        return super(ControlPrenatalExcelReportView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        accion = self.kwargs.get('accion_id', None)
        report = reports.ControlPrenatalExcelReport(self.control)
        identifier = hashlib.md5(b'cp_{}'.format(self.control.id))
        if accion == '1':
            output = self.get_book(report)
            return report.signed_report(identifier.hexdigest(), self.request.META.get('HTTP_REFERER', '/'), output)
        elif accion == "2":
            return report.render_signed_file(identifier.hexdigest())
        else:
            output = self.get_book(report)
            response = HttpResponse(output.read(), content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename={}'.format(self.filename)
            return response

    def get_book(self, report):
        output = StringIO()
        book = report.get_book(output)
        book.close()
        output.seek(0)
        return output


class Fua009ExcelReportView(EstablecimientoRequiredMixin, ExcelView):
    filename = 'Fua_009_{}.xlsx'
    control = None

    def dispatch(self, request, *args, **kwargs):
        self.control = get_object_or_404(Control, id=kwargs.get('control_id'))
        self.filename = self.filename.format(
            self.control.paciente.numero_documento)
        return super(
            Fua009ExcelReportView, self).dispatch(request, *args, **kwargs)

    def get_book(self, output):
        fua = fuas.Fua009ExcelReport(self.control, self.request)
        return fua.get_book(output)


class Fua011ExcelReportView(EstablecimientoRequiredMixin, ExcelView):
    filename = 'Fua_011_{}.xlsx'
    control = None

    def dispatch(self, request, *args, **kwargs):
        self.control = get_object_or_404(Control, id=kwargs.get('control_id'))
        self.filename = self.filename.format(
            self.control.paciente.numero_documento)
        return super(
            Fua011ExcelReportView, self).dispatch(request, *args, **kwargs)

    def get_book(self, output):
        fua = fuas.Fua011ExcelReport(self.control, self.request)
        return fua.get_book(output)


class Fua013ExcelReportView(EstablecimientoRequiredMixin, ExcelView):
    filename = 'Fua_013_{}.xlsx'
    control = None

    def dispatch(self, request, *args, **kwargs):
        self.control = get_object_or_404(Control, id=kwargs.get('control_id'))
        self.filename = self.filename.format(
            self.control.paciente.numero_documento)
        return super(
            Fua013ExcelReportView, self).dispatch(request, *args, **kwargs)

    def get_book(self, output):
        fua = fuas.Fua013ExcelReport(self.control, self.request)
        return fua.get_book(output)


class Fua024ExcelReportView(EstablecimientoRequiredMixin, ExcelView):
    filename = 'Fua_024_{}.xlsx'
    control = None

    def dispatch(self, request, *args, **kwargs):
        self.control = get_object_or_404(Control, id=kwargs.get('control_id'))
        self.filename = self.filename.format(
            self.control.paciente.numero_documento)
        return super(
            Fua024ExcelReportView, self).dispatch(request, *args, **kwargs)

    def get_book(self, output):
        fua = fuas.Fua024ExcelReport(self.control, self.request)
        return fua.get_book(output)


class Fua071ExcelReportView(EstablecimientoRequiredMixin, ExcelView):
    filename = 'Fua_071_{}.xlsx'
    control = None

    def dispatch(self, request, *args, **kwargs):
        self.control = get_object_or_404(Control, id=kwargs.get('control_id'))
        self.filename = self.filename.format(
            self.control.paciente.numero_documento)
        return super(
            Fua071ExcelReportView, self).dispatch(request, *args, **kwargs)

    def get_book(self, output):
        fua = fuas.Fua071ExcelReport(self.control, self.request)
        return fua.get_book(output)
