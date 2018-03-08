# encoding=utf-8
from datetime import datetime, timedelta, time, date

from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings
from django.db.models import Q

from embarazos.models import Embarazo
from controles.models import Control


class Cita(models.Model):
    DURATION = 30  # minutes

    TIPO_CONTROL = 'control'
    TIPO_GESTACION = 'gestacion'

    TIPO_CHOICES = (
        (TIPO_CONTROL, 'Tipo Control'),
        (TIPO_GESTACION, 'Tipo gestación'),)

    ORIGEN_INTERNO = 'interno'
    ORIGEN_EXTERNO = 'externo'

    ORIGEN_CHOICES = (
        (ORIGEN_INTERNO, 'Interno'),
        (ORIGEN_EXTERNO, 'Externo'),)

    origen = models.CharField(
        choices=ORIGEN_CHOICES, default='interno', max_length=10)

    codigo_origen_externo = models.CharField(max_length=10, null=True, blank=True)

    paciente = models.ForeignKey('pacientes.Paciente', related_name='citas')
    # only use for control case
    control = models.ForeignKey(
        'controles.Control', related_name='citas', null=True, blank=True)
    establecimiento = models.ForeignKey(
        'establecimientos.Establecimiento', related_name='citas')
    asistio = models.NullBooleanField(verbose_name='Asistio', default=None)
    tipo = models.CharField(
        'Tipo de cita', choices=TIPO_CHOICES, max_length=10)
    fecha = models.DateTimeField()
    fecha_asistio = models.DateTimeField(null=True, blank=True)
    is_wawared = models.BooleanField(verbose_name='Es Wawared', default=False)
    comentario = models.TextField(
        verbose_name='Comentario', blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    especialista = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False, null=True)
    uuid_cita_minsa = models.CharField(max_length=128, null=True, blank=True)
    is_confirmado_cita_minsa = models.NullBooleanField(default=None)

    class Meta:
        unique_together = ('fecha', 'establecimiento', 'paciente')

    def __unicode__(self):
        return u'{paciente} {fecha}'.format(
            paciente=self.paciente.nombre_completo, fecha=self.fecha)

    def to_event(self):
        return {
            'title': self.paciente.nombre_completo,
            'start': self.fecha.isoformat(),
            'end': (self.fecha + timedelta(minutes=self.DURATION)).isoformat(),
            'url': reverse('cita:edit', kwargs={'id': self.id})
        }

    @classmethod
    def exists_cita_in_same_date(cls, establecimiento, fecha_hora):
        """
        params: establecimiento, fecha_hora:datetime
        """
        return cls.objects.filter(
            establecimiento=establecimiento, fecha=fecha_hora).exists()

    def get_numero_controles(self):
        if self.control:
            return self.control.embarazo.numero_controles
        else:
            return None

    @classmethod
    def get_citas_programadas(cls, establecimiento_id):

        # ids = Embarazo.objects.filter(establecimiento__id=establecimiento_id).values('paciente__id')
        # ids = Embarazo.objects.filter(activo=True).values('paciente__id')

        # ids = [p['paciente__id'] for p in ids]

        _today = datetime.today()

        return cls.objects.filter(
            Q(establecimiento__id=establecimiento_id, fecha__year=_today.year, fecha__month=_today.month,
              fecha__day=_today.day, asistio=None)
            | Q(establecimiento__id=establecimiento_id, fecha__year=_today.year, fecha__month=_today.month,
                fecha__day=_today.day, asistio=False)).order_by('fecha')

    @classmethod
    def get_citas_vencidas(cls, establecimiento_id):

        tmp_lista = []
        # ids = Embarazo.objects.filter(establecimiento__id=establecimiento_id).values_list('paciente__id', flat=True).distinct()
        # ids = Embarazo.objects.filter(activo=True).values_list('paciente__id', flat=True).distinct()

        fecha_desde = date.today() - timedelta(days=8)
        fecha_hasta = date.today()
        # tmp = cls.objects.filter(fecha__lte= datetime.today() - timedelta(days=7),tipo=cls.TIPO_CONTROL, paciente__id__in=ids).exclude(asistio=True).order_by('fecha')
        # tmp = cls.objects.filter(establecimiento__id=establecimiento_id, fecha__gte= fecha_desde, fecha__lt = fecha_hasta,tipo=cls.TIPO_CONTROL, paciente__id__in=ids).exclude(asistio=True).order_by('fecha')
        tmp = cls.objects.filter(control__embarazo__activo=True, establecimiento__id=establecimiento_id,
                                 fecha__gte=fecha_desde, fecha__lt=fecha_hasta, tipo=cls.TIPO_CONTROL).exclude(
            asistio=True).order_by('fecha')

        # for id_paciente in ids:
        for cit in tmp:
            id_paciente = cit.paciente.id

            citas_futura = cls.objects.filter(paciente_id=id_paciente, fecha__gte=fecha_hasta, tipo=cls.TIPO_CONTROL)

            if len(citas_futura) > 0:
                continue

            controles_realizadas = Control.objects.filter(paciente_id=id_paciente, atencion_fecha__gte=fecha_hasta)

            if len(controles_realizadas) > 0:
                continue

            count_tmp = tmp.filter(paciente__id=id_paciente).count()

            if count_tmp > 0:
                if count_tmp > 1:
                    tmp_lista.append(
                        tmp.filter(paciente__id=id_paciente).order_by(
                            '-fecha').first())
                else:
                    tmp_lista.append(tmp.get(paciente__id=id_paciente))

        return tmp_lista

    @classmethod
    def get_next_available_hour_for_day(cls, establecimiento, date):
        cita = cls.objects.filter(
            establecimiento=establecimiento, fecha__year=date.year,
            fecha__month=date.month, fecha__day=date.day
        ).order_by('-fecha').first()
        if cita is None:
            return time(9, 0)
        else:
            return (cita.fecha + timedelta(minutes=cls.DURATION)).time()

    @classmethod
    def schedule_appointment(cls, control):
        cita = cls()
        cita.control = control
        cita.paciente = control.paciente
        cita.origen = cls.ORIGEN_INTERNO
        cita.establecimiento = control.establecimiento
        cita.tipo = cls.TIPO_CONTROL
        fecha = datetime.combine(
            control.proxima_cita, cls.get_next_available_hour_for_day(
                control.establecimiento, control.proxima_cita))
        cita.fecha = fecha
        cita.is_wawared = True
        cita.asistio = False
        cita.save()

    @classmethod
    def exists_cita_in_same_date_for_medical_specialist(cls, establecimiento, fecha_hora, user):
        """
        params: establecimiento, fecha_hora:datetime
        """
        return cls.objects.filter(
            establecimiento=establecimiento, fecha=fecha_hora, especialista=user).exists()

    @classmethod
    def get_citas_programadas_for_medical_specialist(cls, establecimiento_id, user):
        '''_today = datetime.today()
        return cls.objects.filter(
            fecha__year=_today.year, fecha__month=_today.month,
            fecha__day=_today.day,
            asistio=False,
            establecimiento__id=establecimiento_id,
            especialista=user).order_by('fecha')'''

        _today = datetime.today()

        return cls.objects.filter(
            Q(establecimiento__id=establecimiento_id, fecha__year=_today.year, fecha__month=_today.month,
              fecha__day=_today.day, especialista=user, asistio=None)
            | Q(establecimiento__id=establecimiento_id, fecha__year=_today.year, fecha__month=_today.month,
                fecha__day=_today.day, especialista=user, asistio=False)).order_by('fecha')

    @classmethod
    def get_citas_vencidas_for_medical_specialist(cls, establecimiento_id, user):
        '''tmp = cls.objects.filter(fecha__lte=datetime.today() - timedelta(days=7),tipo=cls.TIPO_CONTROL, establecimiento__id=establecimiento_id, especialista=user).exclude(asistio=True).order_by('fecha')
        return tmp'''
        tmp_lista = []
        # ids = Embarazo.objects.filter(establecimiento__id=establecimiento_id).values_list('paciente__id', flat=True).distinct()
        # ids = Embarazo.objects.filter(activo=True).values_list('paciente__id', flat=True).distinct()

        fecha_desde = date.today() - timedelta(days=8)
        fecha_hasta = date.today()
        # tmp = cls.objects.filter(fecha__lte= datetime.today() - timedelta(days=7),tipo=cls.TIPO_CONTROL, paciente__id__in=ids).exclude(asistio=True).order_by('fecha')
        # tmp = cls.objects.filter(establecimiento__id=establecimiento_id, fecha__gte= fecha_desde, fecha__lt = fecha_hasta,tipo=cls.TIPO_CONTROL, especialista=user, paciente__id__in=ids).exclude(asistio=True).order_by('fecha')
        tmp = cls.objects.filter(control__embarazo__activo=True, establecimiento__id=establecimiento_id,
                                 fecha__gte=fecha_desde, fecha__lt=fecha_hasta, tipo=cls.TIPO_CONTROL,
                                 especialista=user).exclude(asistio=True).order_by('fecha')

        # for id_paciente in ids:
        for cit in tmp:
            id_paciente = cit.paciente.id

            citas_futura = cls.objects.filter(paciente_id=id_paciente, fecha__gte=fecha_hasta, tipo=cls.TIPO_CONTROL)

            if len(citas_futura) > 0:
                continue

            controles_realizadas = Control.objects.filter(paciente_id=id_paciente, atencion_fecha__gte=fecha_hasta)

            if len(controles_realizadas) > 0:
                continue

            count_tmp = tmp.filter(paciente__id=id_paciente).count()

            if count_tmp > 0:
                if count_tmp > 1:
                    tmp_lista.append(
                        tmp.filter(paciente__id=id_paciente).order_by(
                            '-fecha').first())
                else:
                    tmp_lista.append(tmp.get(paciente__id=id_paciente))
        return tmp_lista

    @classmethod
    def get_next_available_hour_for_day_for_medical_specialist(cls, establecimiento, date, user):
        cita = cls.objects.filter(
            establecimiento=establecimiento, fecha__year=date.year,
            fecha__month=date.month, fecha__day=date.day, especialista=user
        ).order_by('-fecha').first()
        if cita is None:
            return time(9, 0)
        else:
            return (cita.fecha + timedelta(minutes=cls.DURATION)).time()
