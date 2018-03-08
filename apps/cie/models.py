# -*- coding: utf-8 -*-
from django.db import models

from .managers import ICD10Manager, ICD10ManagerMedical


class ICD10Base(models.Model):
    codigo = models.CharField(
        verbose_name=u'Código',
        max_length=6,
        unique=True,
        db_index=True)
    nombre = models.CharField(u'Nombre', max_length=256)
    nombre_mostrar = models.CharField(
        u'Nombre mostrar', max_length=256, blank=True)
    is_activo = models.BooleanField(default=True)
    is_familia = models.BooleanField(default=True)
    is_medico = models.BooleanField(default=True)
    is_icd10 = models.BooleanField(default=True)

    def __unicode__(self):
        return u'({0}) {1}'.format(self.codigo, self.nombre)

    @property
    def nombre_display(self):
        return self.nombre_mostrar if self.nombre_mostrar else self.nombre


class ICD10(ICD10Base):
    objects = ICD10Manager()

    class Meta:
        proxy = True


class ICD10Medical(ICD10Base):
    objects = ICD10ManagerMedical()

    class Meta:
        proxy = True
