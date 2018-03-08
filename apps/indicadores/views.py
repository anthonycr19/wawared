# -*- coding: utf-8 -*-
# Python imports
from datetime import datetime, timedelta, date

# Django imports
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils import timezone
from django.views.generic import FormView

# Third party apps imports


# Local imports
from controles.models import Control
from dashboard.views import EstablecimientoRequiredMixin
from establecimientos.models import Establecimiento, Diresa, Red, Microred

from .forms import IndicadoresForm


# Create your views here.
class IndexFormView(EstablecimientoRequiredMixin, FormView):
    form_class = IndicadoresForm
    template_name = 'indicadores/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexFormView, self).get_context_data(**kwargs)
        diresa = self.request.GET.get('diresa')
        establecimiento = self.request.GET.get('establecimiento')
        microred = self.request.GET.get('microred')
        red = self.request.GET.get('red')
        if self.request.GET.get('fecha_inicio') is None:
            fecha_inicio = None
        else:
            fecha_inicio = datetime.strptime(
                self.request.GET.get('fecha_inicio'), '%d/%m/%Y').date()
        if self.request.GET.get('fecha_final') is None:
            fecha_final = None
        else:
            fecha_final = datetime.strptime(
                self.request.GET.get('fecha_final'), '%d/%m/%Y').date()

        if establecimiento is None or establecimiento == '':
            if microred is None or microred == '':
                if red is None or red == '':
                    try:
                        alcance = Diresa.objects.get(id=diresa)
                    except Diresa.DoesNotExist:
                        alcance = Diresa.objects.get(id=1)

                    controles = Control.objects.filter(
                        establecimiento__diresa=alcance)
                else:
                    alcance = Red.objects.get(id=red)
                    controles = Control.objects.filter(
                        establecimiento__red=alcance)
            else:
                alcance = Microred.objects.get(id=microred)
                controles = Control.objects.filter(
                    establecimiento__microred=alcance)
        else:
            alcance = Establecimiento.objects.get(id=establecimiento)
            controles = Control.objects.filter(establecimiento=alcance)

        tipo_alcance = alcance.__class__.__name__

        if fecha_inicio is not None and fecha_final is not None:
            controles = controles.filter(
                atencion_fecha__gte=fecha_inicio,
                atencion_fecha__lte=fecha_final)

        indicador = self.request.GET.get('indicador')
        indicador_mensual = True

        # Gestante tamizada con prueba rapida para Sífilis
        if indicador == '6':
            controles = controles.exclude(
                laboratorio__rapida_sifilis='no se hizo')

        # Gestante Adolescente Atendida
        elif indicador == '7':
            today_date = timezone.now()
            controles = controles.filter(
                Q(paciente__fecha_nacimiento__gt=date(
                    year=today_date.year - 18, month=today_date.month,
                    day=today_date.day)) &
                Q(paciente__fecha_nacimiento__lt=date(
                    year=today_date.year - 12, month=today_date.month,
                    day=today_date.day)) &
                Q(numero=1))

        # Gestante Adolescente Controlada
        elif indicador == '8':
            today_date = timezone.now()
            controles = controles.filter(
                Q(paciente__fecha_nacimiento__gt=date(
                    year=today_date.year - 18, month=today_date.month,
                    day=today_date.day)) &
                Q(paciente__fecha_nacimiento__lt=date(
                    year=today_date.year - 12, month=today_date.month,
                    day=today_date.day)) &
                Q(numero=6))

        # Gestante Atendida
        elif indicador == '9':
            controles = controles.filter(numero=1)

        # Gestante Atendida en Psicoprofilaxis y Estimulación Prenatal
        elif indicador == '10':
            controles = controles.filter(
                Q(edad_gestacional_semanas__gt=29) & ~
                Q(psicoprofilaxis_fecha_1=None))

        # Gestante Atendidas por trimestre
        elif indicador == '11':
            indicador_mensual = False
            controles = controles.filter(numero=1)

        # Gestante con ácido fólico 1er trimestre
        elif indicador == '16':
            controles = controles.filter(
                Q(indicacion_acido_folico__gt=0) |
                Q(edad_gestacional_semanas__lt=14))

        # Gestante con Amenaza de Aborto
        elif indicador == '17':
            controles = controles.filter(
                ~Q(examen_fisico__eg_dolor='n/a') | ~
                Q(examen_fisico__eg_posicion='n/a') | ~
                Q(examen_fisico__eg_restos='n/a') |
                Q(examen_fisico__eg_culdocentesis=True) | ~
                Q(examen_fisico__eg_fondo_de_saco='n/a') |
                Q(examen_fisico__eg_mal_olor=True))

        # Gestante con Anemia
        elif indicador == '19':
            controles = controles.filter(
                Q(laboratorio__rapida_hemoglobina_resultado__lt=10) |
                Q(laboratorio__hemoglobina_1_resultado__lt=10) |
                Q(laboratorio__hemoglobina_2_resultado__lt=10) |
                Q(laboratorio__hemoglobina_alta_resultado__lt=10))

        # Gestante con ecografía
        elif indicador == '20':
            controles = controles.filter(ic_ecografia=True)

        # Gestante con evaluación nutricional
        elif indicador == '21':
            controles = controles.filter(ic_nutricion=True)

        # Gestante con PAP
        elif indicador == '23':
            controles = controles.filter(numero=1).exclude(
                laboratorio__pap='no se hizo')

        # Gestante con PAP positivo
        elif indicador == '24':
            controles = controles.filter(laboratorio__pap='anormal')

        # Gestante con Pre Eclampsia
        elif indicador == '25':
            controles = controles.filter(
                Q(edemas='++') | Q(edemas='+++'),
                Q(reflejos='++') | Q(reflejos='+++'))

        # Gestante con resultados de análisis en 2da APN
        elif indicador == '27':
            controles = controles.filter(
                Q(numero=2) & ~Q(
                    laboratorio__glicemia_1='no se hizo') & ~Q(
                    laboratorio__grupo=None) & ~Q(
                    laboratorio__factor=None) & ~Q(
                    laboratorio__hemoglobina_1=None) & ~Q(
                    laboratorio__examen_completo_orina_1=None))

        # Gestante Controlada (6ta atención)
        elif indicador == '29':
            controles = controles.filter(numero=6)

        # Gestante ITU
        elif indicador == '33':
            controles = controles.filter(
                laboratorio__examen_completo_orina_1='positivo')

        # Gestante Preparada en Psicoprofilaxis y
        # Estimulación Prenatal (6 sesiones)
        elif indicador == '34':
            controles = controles.exclude(psicoprofilaxis_fecha_6=None)

        # Gestante protegida con vacuna antitetánica (2 dosis)
        elif indicador == '35':
            controles = controles.filter(
                paciente__vacuna__antitetanica_segunda_dosis=True)

        # Gestante que inicia Plan de parto
        elif indicador == '39':
            controles = controles.exclude(
                embarazo__plan_parto=None)

        # Gestante reactiva para Sífilis
        elif indicador == '42':
            controles = controles.filter(
                Q(laboratorio__rapida_sifilis='reactivo') |
                Q(laboratorio__rapida_sifilis_2='reactivo'))

        # Gestante reactiva para VIH
        elif indicador == '43':
            controles = controles.filter(
                Q(laboratorio__rapida_vih_1='reactivo') |
                Q(laboratorio__rapida_vih_2='reactivo'))

        # Gestante Reenfocada (paquete completo en 6ta atención)
        elif indicador == '44':
            controles = controles.filter(
                Q(ic_psicologia=True) & Q(ic_medicina=True) &
                Q(ic_nutricion=True) & Q(ic_odontologia=True), ~
                Q(psicoprofilaxis_fecha_1=None) | ~
                Q(psicoprofilaxis_fecha_2=None) | ~
                Q(psicoprofilaxis_fecha_3=None) | ~
                Q(psicoprofilaxis_fecha_4=None) | ~
                Q(psicoprofilaxis_fecha_5=None) | ~
                Q(psicoprofilaxis_fecha_6=None))

        # Gestante tamizada con prueba rapida para  VIH
        elif indicador == '46':
            controles = controles.filter(
                Q(numero=1) & ~Q(laboratorio__rapida_vih_1='no se hizo') | ~
                Q(laboratorio__rapida_vih_2='no se hizo'))

        indicador_nombre = None

        for indicador_item in IndicadoresForm.INDICADORES_CHOICES:
            if unicode(indicador_item[0]) == indicador:
                indicador_nombre = indicador_item[1]

        context.update({
            'alcance': alcance.nombre,
            'indicador': indicador,
            'menu': 'indicadores',
            'tipo_alcance': tipo_alcance,
            'tipo_indicador': indicador_mensual,
            'indicador_nombre': indicador_nombre
        })

        try:
            diferencia = fecha_final - fecha_inicio
        except:
            diferencia = None

        indicadores_intervalo = None
        controles_intervalo = None
        fecha_aux = fecha_inicio

        first = True
        equal_dates = 0

        if fecha_aux is not None:
            first = False

        if not first:
            if indicador_mensual:
                json_indicadores = []
                tmp = {}

                while (fecha_aux <= fecha_final and equal_dates == 0):
                    indicadores_intervalo = controles
                    tmp['intervalo_fecha'] = fecha_aux
                    controles_intervalo = Control.objects.filter(
                        establecimiento=alcance, atencion_fecha__gte=fecha_aux)
                    indicadores_intervalo = indicadores_intervalo.filter(
                        atencion_fecha__gte=fecha_aux)

                    if diferencia is not None and \
                            diferencia < timedelta(days=730):
                        try:
                            fecha_aux = fecha_aux.replace(
                                month=fecha_aux.month + 1, day=1)
                        except ValueError as ve:
                            fecha_aux = fecha_aux.replace(
                                year=fecha_aux.year + 1, month=1, day=1)
                    else:
                        try:
                            fecha_aux = fecha_aux.replace(
                                year=fecha_aux.year + 1, month=1, day=1)
                        except ValueError as ve:
                            print
                            str(ve)

                    fecha_aux -= timedelta(days=1)

                    if fecha_aux < fecha_final:
                        tmp['intervalo_final'] = fecha_aux
                        controles_intervalo = controles_intervalo.filter(
                            atencion_fecha__lte=fecha_aux)
                        indicadores_intervalo = indicadores_intervalo.filter(
                            atencion_fecha__lte=fecha_aux)
                        fecha_aux += timedelta(days=1)
                    else:
                        tmp['intervalo_final'] = fecha_final
                        controles_intervalo = controles_intervalo.filter(
                            atencion_fecha__lte=fecha_final)
                        indicadores_intervalo = indicadores_intervalo.filter(
                            atencion_fecha__lte=fecha_final)
                        equal_dates += 1

                    pacientes_tmp = controles_intervalo.values_list(
                        'paciente', flat=True)
                    indicador_tmp = indicadores_intervalo.values_list(
                        'paciente', flat=True)

                    tmp['total_intervalo'] = list(set(pacientes_tmp)).__len__()
                    tmp['indicador_intervalo'] = list(
                        set(indicador_tmp)).__len__()

                    json_indicadores.append(tmp)
                    tmp = {}

                context.update({
                    'json_indicadores': json_indicadores,
                })
            else:
                json_indicadores_trimestrales = []
                tmp = {}

                while (fecha_aux < fecha_final and not equal_dates):
                    indicadores_intervalo = controles
                    tmp['intervalo_fecha'] = fecha_aux
                    controles_intervalo = Control.objects.filter(
                        establecimiento=alcance, atencion_fecha__gte=fecha_aux)
                    indicadores_intervalo = indicadores_intervalo.filter(
                        atencion_fecha__gte=fecha_aux)

                    if diferencia is not None and \
                            diferencia < timedelta(days=730):
                        try:
                            fecha_aux = fecha_aux.replace(
                                month=fecha_aux.month + 1, day=1)
                        except ValueError as ve:
                            fecha_aux = fecha_aux.replace(
                                year=fecha_aux.year + 1, month=1, day=1)
                    else:
                        try:
                            fecha_aux = fecha_aux.replace(
                                year=fecha_aux.year + 1, month=1, day=1)
                        except ValueError as ve:
                            print
                            str(ve)

                    fecha_aux -= timedelta(days=1)

                    if fecha_aux < fecha_final:
                        tmp['intervalo_final'] = fecha_aux
                        controles_intervalo = controles_intervalo.filter(
                            atencion_fecha__lte=fecha_aux)
                        indicadores_intervalo = indicadores_intervalo.filter(
                            atencion_fecha__lte=fecha_aux)
                        fecha_aux += timedelta(days=1)
                    else:
                        tmp['intervalo_final'] = fecha_final
                        controles_intervalo = controles_intervalo.filter(
                            atencion_fecha__lte=fecha_final)
                        indicadores_intervalo = indicadores_intervalo.filter(
                            atencion_fecha__lte=fecha_final)
                        equal_dates += 1

                    indicador_primer_trimestre_tmp = \
                        indicadores_intervalo.filter(
                            edad_gestacional_semanas__lte=12)
                    indicador_segundo_trimestre_tmp = \
                        indicadores_intervalo.filter(
                            edad_gestacional_semanas__gt=12,
                            edad_gestacional_semanas__lte=24)
                    indicador_tercer_trimestre_tmp = \
                        indicadores_intervalo.filter(
                            edad_gestacional_semanas__gt=24,
                            edad_gestacional_semanas__lte=42)

                    primer_tmp = indicador_primer_trimestre_tmp.values_list(
                        'paciente', flat=True)
                    segundo_tmp = indicador_segundo_trimestre_tmp.values_list(
                        'paciente', flat=True)
                    tercer_tmp = indicador_tercer_trimestre_tmp.values_list(
                        'paciente', flat=True)

                    tmp['primer_trimestre'] = list(set(primer_tmp)).__len__()
                    tmp['segundo_trimestre'] = list(set(segundo_tmp)).__len__()
                    tmp['tercer_trimestre'] = list(set(tercer_tmp)).__len__()
                    tmp['total_intervalo'] = tmp['primer_trimestre']
                    tmp['total_intervalo'] += tmp['segundo_trimestre']
                    tmp['total_intervalo'] += tmp['tercer_trimestre']

                    json_indicadores_trimestrales.append(tmp)
                    tmp = {}

                context.update({
                    'json_indicadores_trimestrales':
                        json_indicadores_trimestrales,
                })

        return context

    def get_initial(self):
        diresa = self.request.GET.get('diresa')
        establecimiento = self.request.GET.get('establecimiento')
        fecha_final = self.request.GET.get('fecha_final')
        fecha_inicio = self.request.GET.get('fecha_inicio')
        microred = self.request.GET.get('microred')
        red = self.request.GET.get('red')

        if diresa is None:
            diresa = self.request.user.establecimiento.diresa

        if establecimiento is None:
            establecimiento = self.request.user.establecimiento

        if microred is None:
            microred = self.request.user.establecimiento.microred

        if red is None:
            red = self.request.user.establecimiento.red

        if fecha_inicio is None:
            fecha_inicio = timezone.now().date()

        if fecha_final is None:
            fecha_final = timezone.now().date()

        initial = {
            'diresa': diresa,
            'establecimiento': establecimiento,
            'fecha_final': fecha_final,
            'fecha_inicio': fecha_inicio,
            'indicador': self.request.GET.get('indicador'),
            'microred': microred,
            'red': red
        }
        return initial.copy()

    def get_success_url(self):
        # Aca hacer un redirect a una nueva url donde este el excelview para
        # jalar el excel donde le paso todos los parametros
        query = self.request.POST.copy()
        del query['csrfmiddlewaretoken']
        return reverse('indicadores:index') + '?' + query.urlencode()
