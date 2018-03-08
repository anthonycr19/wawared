# coding=utf-8
from datetime import date
import hashlib

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import IntegrityError, transaction
from django.http import Http404, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DeleteView, DetailView, RedirectView, UpdateView, View

from cie.models import ICD10, ICD10Medical
from dashboard.views import EstablecimientoRequiredMixin, HistoriaClinicaRequiredMixin
from embarazos.reports import FichaTamizajeReport, TamizajeDepresionReport
from establecimientos.models import Establecimiento
from pacientes.models import AntecedenteMedico, Paciente
from .forms import (
    BebeCreateFormset, BebeUpdateFormset, EcografiaDetalleFormSet, EcografiaForm, EmbarazoForm,
    FichaProblemaForm, FichaViolenciaFamiliarForm, PlanPartoForm, UltimoEmbarazoForm)
from .models import (
    Bebe, Ecografia, EcografiaDetalle, Embarazo, FichaProblema, FichaViolenciaFamiliar, PlanParto,
    UltimoEmbarazo)


class UltimosEmbarazosView(EstablecimientoRequiredMixin, HistoriaClinicaRequiredMixin, DetailView):
    template_name = 'embarazos/ultimos_embarazos.html'
    model = Paciente
    pk_url_kwarg = 'paciente_id'
    context_object_name = 'paciente'
    paciente_key = 'paciente_id'

    def get_context_data(self, **kwargs):
        context = super(UltimosEmbarazosView, self).get_context_data(**kwargs)
        context.update({
            'embarazos': UltimoEmbarazo.objects.filter(
                paciente=self.object).order_by('numero')
        })
        return context


class UltimoEmbarazoException(Exception):
    pass


class UltimoEmbarazoMixin(EstablecimientoRequiredMixin):
    model = UltimoEmbarazo
    template_name = 'embarazos/ultimo_embarazo.html'
    form_class = UltimoEmbarazoForm
    paciente = None
    object = None
    formset = None

    def dispatch(self, request, *args, **kwargs):
        try:
            paciente = Paciente.objects.get(id=kwargs.get('paciente_id', None))
            self.paciente = paciente
            return super(
                UltimoEmbarazoMixin, self).dispatch(request, *args, **kwargs)
        except Paciente.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        bebe_formset = self.get_formset()
        return self.render_to_response(
            self.get_context_data(form=form, bebe_formset=bebe_formset))

    def get_form(self):
        obj = self.get_object()
        form = self.form_class(self.request.POST or None, instance=obj)
        return form

    def get_formset(self):
        formset = self.formset(
            self.request.POST or None, instance=self.get_object())
        return formset

    def get_object(self, queryset=None):
        raise NotImplementedError()

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        bebe_formset = self.get_formset()
        if form.is_valid() and bebe_formset.is_valid():
            return self.form_valid(form, bebe_formset)
        else:
            return self.form_invalid(form, bebe_formset)

    def form_valid(self, form, bebe_formset):
        try:
            with transaction.atomic():
                ue = form.save(commit=False)
                ue.paciente = self.paciente
                if not ue.id:
                    ue.establecimiento = Establecimiento.objects.get(
                        id=self.request.session['establecimiento_id'])
                    ue.created_by = self.request.user
                ue.save()
                bebe_formset.instance = ue
                bebe_formset.save()
                if not ue.bebes.count():
                    raise UltimoEmbarazoException(
                        u'Al menos debe registrarse un bebé.')
                if ue.tipo == UltimoEmbarazo.TIPO_UNICO and ue.bebes.count() > 1:
                    raise UltimoEmbarazoException(
                        u'Para agregar más de un bebé debe elegir embarazo multiple.')
                if ue.tipo == UltimoEmbarazo.TIPO_MULTIPLE and ue.bebes.count() < 2:
                    raise UltimoEmbarazoException(
                        u'Para seleccionar embarazo multiple al menos deben registrarse dos bebés.')
                if not ue.is_valid_babies_dates_embarazo_multiple():
                    raise UltimoEmbarazoException(
                        u'La diferencia de dias entre las fechas es inválida.')
                today = date.today()
                if ue.tipo == UltimoEmbarazo.TIPO_MULTIPLE:
                    for bebe in ue.bebes.all():
                        if bebe.terminacion in (Bebe.TERMINACION_VAGINAL, Bebe.TERMINACION_CESAREA):
                            if ue.bebes.filter(fecha=bebe.fecha).count() != ue.bebes.filter(
                                terminacion=bebe.terminacion).count():
                                raise UltimoEmbarazoException(
                                    u'Para la terminacion vaginal o cesarea deben coincidir las fechas.')
                for bebe in ue.bebes.all():
                    if not bebe.no_recuerda_fecha and bebe.fecha > today:
                        raise UltimoEmbarazoException(
                            u'Las fechas no pueden sera mayores a la fecha actual.')
                    if bebe.terminacion == Bebe.TERMINACION_CESAREA:
                        cie = ICD10Medical.objects.get(codigo='Z924')
                        if not AntecedenteMedico.objects.filter(paciente=ue.paciente, cie=cie).exists():
                            AntecedenteMedico.objects.create(
                                paciente=ue.paciente, cie=cie, observacion='')
                        break
                return super(UltimoEmbarazoMixin, self).form_valid(form)
        except UltimoEmbarazoException as ex:
            messages.warning(self.request, ex.message)
            return self.form_invalid(form, bebe_formset)

    def form_invalid(self, form, bebe_formset):
        return self.render_to_response(
            self.get_context_data(form=form, bebe_formset=bebe_formset))

    def get_context_data(self, **kwargs):
        context = super(UltimoEmbarazoMixin, self).get_context_data(**kwargs)
        context.update({
            'paciente': self.paciente
        })
        return context

    def get_success_url(self):

        action = self.request.POST['txt_action']

        if action:
            if action == 'guardar_agregar':
                if self.request.session.get('modulo_control'):
                    return reverse('embarazos:ultimo_embarazo_create', kwargs={
                    'paciente_id': self.paciente.id})
                else:
                    return reverse('partos:embarazos_ultimo_embarazo_create', kwargs={
                    'paciente_id': self.paciente.id})

        UltimoEmbarazo.order_by_date(self.paciente)
        if self.request.session.get('modulo_control'):
            return reverse('embarazos:ultimos_embarazos', kwargs={
            'paciente_id': self.paciente.id})
        else:
            return reverse('partos:embarazos_ultimos_embarazos', kwargs={
            'paciente_id': self.paciente.id})


class UltimoEmbarazoCreateView(UltimoEmbarazoMixin, CreateView):
    formset = BebeCreateFormset
    permissions = ('embarazos.add_ultimoembarazo',)

    def get_object(self, queryset=None):
        return self.model()

    def get_context_data(self, **kwargs):
        context = super(
            UltimoEmbarazoCreateView, self).get_context_data(**kwargs)
        context.update({
            'title': u'Agregar embarazo previo'
        })
        return context


class UltimoEmbarazoFromEmbarazoCreateView(UltimoEmbarazoCreateView):
    permissions = ('embarazos.add_ultimoembarazo',)

    def dispatch(self, request, *args, **kwargs):
        self.embarazo = get_object_or_404(
            Embarazo, id=kwargs.get('embarazo_id', None))
        return super(UltimoEmbarazoFromEmbarazoCreateView, self).dispatch(
            request, *args, **kwargs)

    def get_success_url(self):

        self.object.embarazo = self.embarazo
        self.object.save()
        self.embarazo.activo = False
        self.embarazo.save()

        UltimoEmbarazo.order_by_date(self.paciente)
        messages.success(self.request, 'Embarazo terminado y guardado')

        action = self.request.POST['txt_action']

        if action:
            if action == 'guardar_agregar':
                return reverse('embarazos:create', kwargs={'paciente_id': self.paciente.id})
            else:
                return reverse('paciente:update', kwargs={'id': self.paciente.id})

        return reverse('paciente:update', kwargs={'id': self.paciente.id})


class UltimoEmbarazoUpdateView(UltimoEmbarazoMixin, UpdateView):
    pk_url_kwarg = 'id'
    formset = BebeUpdateFormset
    permissions = ('embarazos.change_ultimoembarazo',)

    def get_object(self, queryset=None):
        if self.object is not None:
            return self.object
        else:
            try:
                ue = UltimoEmbarazo.objects.get(id=self.kwargs.get('id', 0))
                return ue
            except UltimoEmbarazo.DoesNotExist:
                raise Http404

    def get_context_data(self, **kwargs):
        context = super(
            UltimoEmbarazoUpdateView, self).get_context_data(**kwargs)
        context.update({
            'title': u'Editar embarazo previo'
        })
        return context


class UltimoEmbarazoDeleteView(EstablecimientoRequiredMixin, RedirectView):
    permanent = False
    paciente = None

    def dispatch(self, request, *args, **kwargs):
        self.paciente = get_object_or_404(
            Paciente, id=kwargs.get('paciente_id', 0))
        return super(
            UltimoEmbarazoDeleteView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        ue = get_object_or_404(UltimoEmbarazo, id=kwargs.get('id', 0))
        if ue.created.date() < date.today():
            messages.warning(self.request, 'No puede eliminar embarazo anterior')
            return reverse('embarazos:ultimos_embarazos', kwargs={'paciente_id': self.paciente.id})
        ue.delete()
        UltimoEmbarazo.order_by_date(self.paciente)
        messages.success(self.request, u'Embarazo borrado')
        return reverse('embarazos:ultimos_embarazos', kwargs={'paciente_id': self.paciente.id})


class EmbarazoMixin(EstablecimientoRequiredMixin):
    model = Embarazo
    form_class = EmbarazoForm
    paciente = None
    object = None
    success_message = ''

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        ficha_form = self.get_ficha_violencia_familiar_form()
        ficha_problema_form = self.get_ficha_problema_form()
        if form.is_valid() and ficha_form.is_valid() and ficha_problema_form.is_valid():
            return self.form_valid(form, ficha_form, ficha_problema_form)
        else:
            return self.form_invalid(form, ficha_form, ficha_problema_form)

    def form_valid(self, form, ficha_form, ficha_problema_form):
        try:
            with transaction.atomic():
                embarazo = form.save(commit=False)
                embarazo.paciente = self.paciente
                if form.instance.id is None:  # when create instance
                    embarazo.establecimiento_id = self.request.session.get('establecimiento_id')
                embarazo.activo = True
                if not embarazo.id:
                    embarazo.created_by = self.request.user
                embarazo.save()
                embarazo.hospitalizacion_diagnosticos.clear()
                for hd_id in self.request.POST.getlist('hospitalizacion_diagnosticos'):
                    embarazo.hospitalizacion_diagnosticos.add(
                        ICD10.objects.get(id=hd_id))

                embarazo.emergencia_diagnosticos.clear()
                for hd_id in self.request.POST.getlist('emergencia_diagnosticos'):
                    embarazo.emergencia_diagnosticos.add(
                        ICD10.objects.get(id=hd_id))
                ficha = ficha_form.save(commit=False)
                ficha.embarazo = embarazo
                ficha.paciente = self.paciente
                if not ficha.id:
                    ficha.created_by = self.request.user
                ficha.save()
                ficha_problema = ficha_problema_form.save(commit=False)
                ficha_problema.paciente = self.paciente
                ficha_problema.embarazo = embarazo
                if not ficha_problema.id:
                    ficha_problema.created_by = self.request.user
                ficha_problema.save()
        except (IntegrityError, ICD10.DoesNotExist) as ex:
            print
            ex.message  # TODO log this message
            messages.warning(
                self.request, u'Ocurrio un error vuelva a intentarlo')
            return self.form_invalid(form, ficha_form, ficha_problema_form)
        return super(EmbarazoMixin, self).form_valid(form)

    def form_invalid(self, form, ficha_form, ficha_problema_form):
        hospitalizacion_diagnosticos_from_post_data = ICD10.objects.filter(
            id__in=self.request.POST.getlist('hospitalizacion_diagnosticos'))
        emergencia_diagnosticos_from_post_data = ICD10.objects.filter(
            id__in=self.request.POST.getlist('emergencia_diagnosticos'))

        return self.render_to_response(self.get_context_data(
            form=form, ficha_form=ficha_form,
            hospitalizacion_diagnosticos_from_post_data=(
                hospitalizacion_diagnosticos_from_post_data),
            emergencia_diagnosticos_from_post_data=(
                emergencia_diagnosticos_from_post_data),
            ficha_problema_form=ficha_problema_form)
        )

    def get_context_data(self, **kwargs):
        context = super(EmbarazoMixin, self).get_context_data(**kwargs)
        context.update({
            'paciente': self.paciente,
            'ficha_form': self.get_ficha_violencia_familiar_form(),
            'ficha_problema_form': self.get_ficha_problema_form()
        })
        return context

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse('embarazos:ecografias', kwargs={
            'paciente_id': self.paciente.id})

    def get_object(self, queryset=None):
        raise NotImplementedError

    def get_ficha(self):
        raise NotImplementedError

    def get_ficha_problema(self):
        raise NotImplementedError

    def get_ficha_violencia_familiar_form(self):
        form = FichaViolenciaFamiliarForm(
            self.request.POST or None, instance=self.get_ficha())
        return form

    def get_ficha_problema_form(self):
        form = FichaProblemaForm(
            self.request.POST or None, instance=self.get_ficha_problema())
        return form


class EmbarazoCreateView(HistoriaClinicaRequiredMixin, EmbarazoMixin, CreateView):
    paciente_key = 'paciente_id'
    template_name = 'embarazos/embarazo_register.html'
    success_message = u'Embarazo registrado con éxito'
    permissions = ('embarazos.add_embarazo',)

    def dispatch(self, request, *args, **kwargs):
        try:
            paciente = Paciente.objects.get(id=kwargs.get('paciente_id', None))
            self.paciente = paciente
            self.object = self.model()
            try:
                Embarazo.objects.get(paciente=self.paciente, activo=True)
                messages.warning(
                    request,
                    u'La gestante está en módulo de parto')
                return HttpResponseRedirect(reverse(
                    'controles:list', kwargs={'paciente_id': self.paciente.id}))
            except Embarazo.DoesNotExist:
                return super(EmbarazoCreateView, self).dispatch(
                    request, *args, **kwargs)
        except Paciente.DoesNotExist:
            raise Http404

    def get_object(self, queryset=None):
        return self.model()

    def get_ficha(self):
        return FichaViolenciaFamiliar()

    def get_ficha_problema(self):
        return FichaProblema()

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse('partos:ingreso_register', kwargs={'paciente_id': self.paciente.id})


class EmbarazoControlCreateView(HistoriaClinicaRequiredMixin, EmbarazoMixin, CreateView):
    paciente_key = 'paciente_id'
    template_name = 'embarazos/embarazo_control_register.html'
    success_message = u'Embarazo registrado con éxito'
    permissions = ('embarazos.add_embarazo',)

    def dispatch(self, request, *args, **kwargs):
        self.paciente = get_object_or_404(Paciente, id=kwargs.get('paciente_id', 0))
        try:
            Embarazo.objects.get(paciente=self.paciente, activo=True)
            messages.warning(
                request,
                u'La gestante está en módulo de parto')
            return HttpResponseRedirect(reverse(
                'controles:list', kwargs={'paciente_id': self.paciente.id}))
        except Embarazo.DoesNotExist:
            return super(EmbarazoControlCreateView, self).dispatch(
                request, *args, **kwargs)

    def get_object(self, queryset=None):
        embarazo = Embarazo.objects.get(paciente=self.paciente, activo=True)
        return embarazo

    def get_ficha(self):
        # Devuleve el modelo de FichaViolenciaFamiliar
        return FichaViolenciaFamiliar()

    def get_ficha_problema(self):
        # Devuleve el modelo de FichaProblema
        return FichaProblema()

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse('embarazos:ecografia_create', kwargs={'paciente_id': self.paciente.id})


class EmbarazoUpdateCurrentView(HistoriaClinicaRequiredMixin, EmbarazoMixin, UpdateView):
    paciente_key = 'paciente_id'
    template_name = 'embarazos/embarazo_edit.html'
    success_message = u'Se actualizó el embarazo'
    permissions = ('embarazos.change_embarazo',)

    def dispatch(self, request, *args, **kwargs):
        try:  # TODO DRY this
            paciente = Paciente.objects.get(id=kwargs.get('paciente_id', None))
            self.paciente = paciente
            try:
                self.object = Embarazo.objects.get(
                    paciente=self.paciente, activo=True)
                return super(EmbarazoUpdateCurrentView, self).dispatch(
                    request, *args, **kwargs)
            except Embarazo.DoesNotExist:
                messages.warning(request, u'No existe un embarazo activo, debe crear uno primero')
                return HttpResponseRedirect(reverse(
                    'embarazos:create', kwargs={'paciente_id': self.paciente.id}))
        except Paciente.DoesNotExist:
            raise Http404

    def get_object(self, queryset=None):
        return self.object

    def get_ficha(self):
        try:
            ficha = FichaViolenciaFamiliar.objects.get(
                embarazo=self.get_object(), paciente=self.paciente)
        except FichaViolenciaFamiliar.DoesNotExist:
            ficha = FichaViolenciaFamiliar.objects.create(
                created_by=self.request.user, embarazo=self.get_object(),
                paciente=self.paciente)
        return ficha

    def get_ficha_problema(self):
        try:
            ficha = FichaProblema.objects.get(
                embarazo=self.get_object(), paciente=self.paciente)
        except FichaProblema.DoesNotExist:
            ficha = FichaProblema.objects.create(
                created_by=self.request.user, embarazo=self.get_object(),
                paciente=self.paciente)
        return ficha


class ViolenciaGeneroUpdateCurrentView(EmbarazoUpdateCurrentView):
    template_name = 'embarazos/violencia_genero.html'

    def get_ficha_violencia_familiar_form(self):
        form = FichaViolenciaFamiliarForm(
            self.request.POST or None, instance=self.get_ficha())
        return form

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        ficha_form = self.get_ficha_violencia_familiar_form()

        if ficha_form.is_valid():
            ficha_form.save()
            embarazo = Embarazo.objects.get(id=form.instance.id)
            embarazo.numero_cigarros_diarios = form['numero_cigarros_diarios'].value()
            embarazo.usa_drogas = form['usa_drogas'].value()
            embarazo.save()

            return HttpResponseRedirect(reverse('controles:list', kwargs={'paciente_id': self.paciente.id}))
        else:
            context = self.get_context_data(form=form)
            return self.render_to_response(context)

    def get_form(self, form_class):
        return form_class(
            self.request.POST or None, instance=self.get_object())

    def get_object(self, queryset=None):
        return self.object


class EcografiasView(EstablecimientoRequiredMixin, HistoriaClinicaRequiredMixin, DetailView):
    template_name = 'embarazos/ecografias.html'
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
            return super(EcografiasView, self).get(request, *args, **kwargs)
        except Embarazo.DoesNotExist:
            return HttpResponseRedirect(
                reverse('embarazos:create', kwargs={'id': paciente.id}))

    def get_context_data(self, **kwargs):
        context = super(EcografiasView, self).get_context_data(**kwargs)
        context.update({
            'ecografias': Ecografia.objects.filter(
                embarazo=self.embarazo).order_by('numero')
        })
        return context


class EcografiaMixin(EstablecimientoRequiredMixin):
    model = Ecografia
    form_class = EcografiaForm
    embarazo = None
    paciente = None
    title = ''
    success_message = ''

    def dispatch(self, request, *args, **kwargs):
        paciente = self.get_paciente(**kwargs)
        self.paciente = paciente
        try:
            embarazo = Embarazo.objects.get(paciente=paciente, activo=True)
            self.embarazo = embarazo
            return super(
                EcografiaMixin, self).dispatch(request, *args, **kwargs)
        except Embarazo.DoesNotExist:
            messages.warning(
                request,
                u'No existe un embarazo activo, debe crear uno primero')
            return HttpResponseRedirect(reverse(
                'embarazos:create', kwargs={'paciente_id': paciente.id}))

    def get_ecografia_detalle_formset(self):
        return EcografiaDetalleFormSet(self.request.POST or None, instance=self.object)

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        eco_formset = context['eco_formset']

        if not form.is_valid() or not eco_formset.is_valid():
            context = self.get_context_data(form=form)
            context['eco_formset'] = eco_formset
            return self.render_to_response(context)

        ecografia = form.save(commit=False)
        ecografia.embarazo = self.embarazo
        ecografia.establecimiento_id = self.request.session['establecimiento_id']

        if not ecografia.id:
            ecografia.created_by = self.request.user
        ecografia.save()

        if ecografia.id:
            for eco_form in eco_formset:
                if not eco_form.get_eliminado():
                    member = eco_form.save(commit=False)
                    member.ecografia = ecografia
                    member.save()
                else:
                    if eco_form.instance.id:
                        eco_form.instance.delete()

        return super(EcografiaMixin, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EcografiaMixin, self).get_context_data(**kwargs)

        if self.object:
            ecogarfia_detalles = EcografiaDetalle.objects.filter(ecografia=self.object)

            if len(ecogarfia_detalles) == 0:
                detalle_ecografia = EcografiaDetalle()
                detalle_ecografia.ecografia = self.object
                detalle_ecografia.biometria_fetal = self.object.biometria_fetal
                detalle_ecografia.created = self.object.created

                detalle_ecografia.save()

        eco_formset = self.get_ecografia_detalle_formset()

        context.update({
            'paciente': self.paciente,
            'title': self.title,
            'embarazo': self.embarazo,
            'eco_formset': eco_formset
        })
        return context

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        Ecografia.order_by_date(self.embarazo)
        return reverse('controles:list', kwargs={'paciente_id': self.paciente.id})

    def get_paciente(self, **kwargs):
        try:
            paciente = Paciente.objects.get(id=kwargs.get('paciente_id', 0))
            return paciente
        except Paciente.DoesNotExist:
            raise Http404


class EcografiaCreateView(HistoriaClinicaRequiredMixin, EcografiaMixin, CreateView):
    template_name = 'embarazos/ecografia.html'
    success_message = u'Se agrego la ecografia al embarazo actual'
    title = u'Agregar ecografia al embarazo actual'
    paciente_key = 'paciente_id'
    permissions = ('embarazos.add_ecografia',)

    def get_ecografia_detalle_formset(self):
        return EcografiaDetalleFormSet(self.request.POST or None, instance=self.object)

    def get_context_data(self, **kwargs):
        context = super(EcografiaCreateView, self).get_context_data(**kwargs)
        eco_formset = self.get_ecografia_detalle_formset()

        context.update({
            'eco_formset': eco_formset,
        })

        return context

    def get_form(self, form_class):

        form = super(EcografiaCreateView, self).get_form(form_class)
        last_ecografia = self.embarazo.ecografias.last()
        if last_ecografia is not None:
            form.fields['tipo_embarazo'].initial = last_ecografia.tipo_embarazo
        return form

    def get_success_url(self):

        if self.object.id:
            messages.success(self.request, self.success_message)
            Ecografia.order_by_date(self.embarazo)

        return reverse(
            'controles:create', kwargs={'embarazo_id': self.embarazo.id})

        '''if self.embarazo.ecografias.count() == 1:
            return reverse(
                'controles:create', kwargs={'embarazo_id': self.embarazo.id})
        else:
            return reverse(
                'embarazos:ecografias',
                kwargs={'paciente_id': self.paciente.id})'''


class EcografiaUpdateView(HistoriaClinicaRequiredMixin, EcografiaMixin, UpdateView):
    template_name = 'embarazos/ecografia.html'
    pk_url_kwarg = 'id'
    success_message = u'se actualizo la ecografia'
    title = u'Actualizar ecografia'
    paciente_key = 'paciente_id'
    permissions = ('embarazos.change_ecografia',)


class FichaTamizajeReportView(View):
    def get(self, request, *args, **kwargs):
        accion = kwargs.get('accion_id', None)
        embarazo = get_object_or_404(
            Embarazo, id=kwargs.get('embarazo_id', ''))
        report = FichaTamizajeReport(embarazo)
        identifier = hashlib.md5(b'tv_{}'.format(embarazo.id))
        if accion == '1':
            return report.signed_report(identifier.hexdigest(), request.META.get('HTTP_REFERER', '/'))
        elif accion == "2":
            return report.render_signed_file(identifier.hexdigest())
        else:
            return report.render_to_response()


class TamizajeDepresionReportView(View):
    def get(self, request, *args, **kwargs):
        embarazo = get_object_or_404(
            Embarazo, id=kwargs.get('embarazo_id', ''))
        report = TamizajeDepresionReport(embarazo)
        return report.render_to_response()


class PlanPartoUpdateView(EstablecimientoRequiredMixin, UpdateView):
    model = PlanParto
    form_class = PlanPartoForm
    template_name = 'embarazos/plan_parto.html'
    object = None
    paciente = None
    embarazo = None
    context_object_name = 'plan_parto'
    permissions = ('embarazos.change_planparto',)

    def dispatch(self, request, *args, **kwargs):
        self.embarazo = get_object_or_404(
            Embarazo, id=kwargs.get('embarazo_id', None))
        try:
            self.object = PlanParto.objects.get(embarazo=self.embarazo)
        except PlanParto.DoesNotExist:
            self.object = PlanParto.objects.create(
                created_by=request.user, embarazo=self.embarazo,
                establecimiento_id=request.session['establecimiento_id'])

            pac = self.embarazo.paciente
            if pac.telefono:
                self.object.telefono = pac.telefono
            elif pac.celular:
                self.object.telefono = pac.celular
            elif pac.celular2:
                self.object.telefono = pac.celular2

            self.object.e1_fecha = date.today()

        return super(
            PlanPartoUpdateView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.object

    def get_context_data(self, **kwargs):
        context = super(PlanPartoUpdateView, self).get_context_data(**kwargs)
        context.update({
            'paciente': self.get_object().embarazo.paciente,
            'title': 'Plan de parto'
        })
        return context

    def get_success_url(self):
        messages.success(self.request, 'Plan de parto guardado')
        return reverse(
            'embarazos:plan_parto',
            kwargs={'embarazo_id': self.embarazo.id}) + '?success=1'


class PlanPartoView(PlanPartoUpdateView):
    def post(self, request, *args, **kwargs):
        return HttpResponseNotAllowed('')


class TerminarEmbarazoView(EstablecimientoRequiredMixin, RedirectView):
    permanent = False
    permissions = ('embarazos.change_embarazo',)

    def get_redirect_url(self, *args, **kwargs):
        paciente = get_object_or_404(
            Paciente, id=kwargs.get('paciente_id', None))
        embarazo = get_object_or_404(
            Embarazo, id=kwargs.get('embarazo_id', None))
        messages.warning(self.request, 'Registre el resultado del embarazo')
        return reverse(
            'embarazos:ultimo_embarazo_from_embarazo_create',
            kwargs={'paciente_id': paciente.id, 'embarazo_id': embarazo.id})


class EcografiaDeleteView(DeleteView):
    model = Ecografia
    pk_url_kwarg = 'id'
    paciente_key = 'paciente_id'

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        if self.object.created.date() < date.today():
            messages.warning(self.request, 'No puede eliminar ecografía anterior')
            return HttpResponseRedirect(reverse(
                'embarazos:ecografias', kwargs={'paciente_id': self.kwargs.get('paciente_id')}))
        return self.post(*args, **kwargs)

    def get_success_url(self):
        return reverse(
            'embarazos:ecografias',
            kwargs={'paciente_id': self.kwargs.get('paciente_id')})
