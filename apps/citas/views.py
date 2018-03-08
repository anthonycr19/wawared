from datetime import datetime

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.http.response import JsonResponse
from django.views.generic import (
    FormView, View, TemplateView, UpdateView, RedirectView, )

from dashboard.views import EstablecimientoRequiredMixin
from establecimientos.models import Establecimiento
from pacientes.models import Paciente, HistoriaClinica

from .forms import CitaRegisterForm, CitaForm
from .models import Cita


class CitasCalendarView(EstablecimientoRequiredMixin, TemplateView):
    template_name = 'citas/calendar.html'


class CitaCreateView(EstablecimientoRequiredMixin, FormView):
    template_name = 'citas/register.html'
    form_class = CitaRegisterForm
    selected = False
    paciente = None
    establecimiento = None
    permissions = ('citas.add_cita',)

    def get_form(self, form_class):
        form = super(CitaCreateView, self).get_form(form_class)
        form.fields['paciente'].queryset = Paciente.objects.all()
        selected = self.get_selected_paciente()
        if selected:
            form.fields['paciente'].initial = selected
            self.selected = True
            self.paciente = selected
        return form

    def form_valid(self, form):
        cita = form.save(commit=False)
        establecimiento = Establecimiento.objects.get(
            id=self.request.session['establecimiento_id'])
        cita.establecimiento = establecimiento
        cita.tipo = Cita.TIPO_GESTACION
        cita.is_wawared = False
        cita.asistio = False
        cita.fecha = datetime.combine(
            form.cleaned_data['cita_fecha'], form.cleaned_data['cita_hora'])
        if not Cita.exists_cita_in_same_date(establecimiento, cita.fecha):
            cita.save()
            messages.success(
                self.request, u'Se agrego la cita {}'.format(cita))
            self.success_url = reverse('dashboard_home')
        else:
            self.success_url = ''.join([
                reverse('cita:register'), '?selected=', str(self.paciente.id)])
            messages.warning(self.request, u'Fecha y hora ya asignadas')
        return super(CitaCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CitaCreateView, self).get_context_data(**kwargs)
        context.update({
            'menu': 'registrar cita',
            'pacientes': self.get_pacientes(),
            'selected': self.selected,
            'paciente': self.paciente,
            'establecimiento': self.establecimiento
        })
        if self.request.GET.get('q'):
            context['establecimientos'] = Establecimiento.objects.all()
        return context

    def get_selected_paciente(self):
        paciente_id = self.request.GET.get('selected', '')
        try:
            paciente = Paciente.objects.get(id=paciente_id)
            return paciente
        except (Paciente.DoesNotExist, ValueError):
            return None

    def get_pacientes(self):
        q = self.request.GET.get('q', None)
        if q is not None:
            hc_qs = HistoriaClinica.objects.filter(
                numero__icontains=q).values('paciente__id')
            ids = [hc['paciente__id'] for hc in hc_qs]
            paciente_qs = Paciente.objects.filter(
                Q(nombres__icontains=q) | Q(numero_documento__icontains=q) |
                Q(apellido_paterno__icontains=q) |
                Q(apellido_materno__icontains=q)).values('id')
            ids += [p['id'] for p in paciente_qs]
            return Paciente.objects.filter(id__in=ids)
        else:
            return Paciente.objects.none()


class CitaUpdateView(EstablecimientoRequiredMixin, UpdateView):
    template_name = 'citas/edit.html'
    model = Cita
    form_class = CitaForm
    context_object_name = 'cita'
    pk_url_kwarg = 'id'
    permissions = ('citas.change_cita',)

    def get_form(self, form_class):
        form = super(CitaUpdateView, self).get_form(form_class)
        form.fields['cita_fecha'].initial = form.instance.fecha.date()
        form.fields['cita_hora'].initial = form.instance.fecha.time()
        return form

    def form_valid(self, form):
        cita = form.save(commit=False)
        cita.fecha = datetime.combine(
            form.cleaned_data['cita_fecha'], form.cleaned_data['cita_hora'])
        if not Cita.exists_cita_in_same_date(cita.establecimiento, cita.fecha):
            cita.save()
            return super(CitaUpdateView, self).form_valid(form)
        else:
            messages.warning(self.request, u'Fecha y hora ya asignadas')
            return HttpResponseRedirect(
                reverse('cita:edit', kwargs={'id': cita.id}))

    def get_success_url(self):
        messages.success(self.request, u'Cita actualizada')
        return reverse('dashboard_home')


class CitaDeleteView(EstablecimientoRequiredMixin, RedirectView):
    permanent = False
    permissions = ('citas.delete_cita',)

    def get_redirect_url(self, **kwargs):
        try:
            cita = Cita.objects.get(id=kwargs.get('id', 0))
            cita.delete()
            messages.success(self.request, u'Cita eliminada')
            return reverse('dashboard_home')
        except Cita.DoesNotExist:
            raise Http404


class CitasEventJsonView(EstablecimientoRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        events = []

        establecimiento_actual = Establecimiento.objects.get(id=request.session['establecimiento_id'])
        if establecimiento_actual.is_sistema_externo_admision:
            lista = Cita.objects.filter(fecha__gte=datetime.today(),
                                        establecimiento_id=request.session['establecimiento_id'],
                                        especialista=request.user).exclude(asistio=True)
        else:
            lista = Cita.objects.filter(fecha__gte=datetime.today(),
                                        establecimiento_id=request.session['establecimiento_id']).exclude(asistio=True)

        for cita in lista:
            events.append(cita.to_event())

        return JsonResponse(events, safe=False)
