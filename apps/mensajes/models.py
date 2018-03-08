# coding: utf-8
from __future__ import unicode_literals
from datetime import datetime
from datetime import timedelta

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models


# Create your models here.


class Mensajes(models.Model):
    MENSAJE_REGEX = RegexValidator(
        regex=r'^[0-9a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.\'-]+$',
        message=u'Solo caracteres validos')

    Mensaje_Gestante = 'gestante'
    Mensaje_Purperio = 'puerperio'

    MENSAJE_CHOICES = (
        (Mensaje_Gestante, u'Gestante'),
        (Mensaje_Purperio, u'Puerperio'),
    )

    Mensaje_dia1 = 0
    Mensaje_dia2 = 1
    Mensaje_dia3 = 2
    Mensaje_dia4 = 3
    Mensaje_dia5 = 4
    Mensaje_dia6 = 5
    Mensaje_dia7 = 6

    MENSAJE_DIA_SEMANA_CHOICES = (
        (Mensaje_dia1, u'Lunes'),
        (Mensaje_dia2, u'Martes'),
        (Mensaje_dia3, u'Miercoles'),
        (Mensaje_dia4, u'Jueves'),
        (Mensaje_dia5, u'Viernes'),
        (Mensaje_dia6, u'Sabado'),
        (Mensaje_dia7, u'Domingo'),
    )

    semana_mensaje = models.IntegerField(u'Semana', blank=False, null=False, default=0,
                                         validators=[MinValueValidator(1), MaxValueValidator(52)])
    dia_semana = models.IntegerField(u'Dia de semana', blank=False, null=False, choices=MENSAJE_DIA_SEMANA_CHOICES,
                                     default=Mensaje_dia1, validators=[MinValueValidator(0), MaxValueValidator(6)])
    tipo_mensaje = models.CharField(u'Tipo', max_length=10, choices=MENSAJE_CHOICES, null=False,
                                    default=Mensaje_Gestante)
    mensaje = models.CharField(u'Mensaje', max_length=200, blank=False, null=False, validators=[MENSAJE_REGEX])

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = u'Mensaje'
        verbose_name_plural = u'Mensajes'
        unique_together = ('semana_mensaje', 'dia_semana', 'tipo_mensaje')

    def __unicode__(self):
        return u'{mensaje}'.format(
            mensaje=self.mensaje)
