# -*- coding: utf-8 -*-

from django.db import models


class Pais(models.Model):
    codigo = models.CharField(verbose_name='Codigo', max_length=3)
    nombre = models.CharField(
        max_length=100, verbose_name='Nombre', null=False)

    class Meta:
        verbose_name = u'País'
        verbose_name_plural = u'Paises'

    def __unicode__(self):
        return self.nombre


class Departamento(models.Model):
    codigo = models.CharField(verbose_name='Codigo', max_length=6, blank=True)
    nombre = models.CharField(
        max_length=100, verbose_name='Nombre', null=False)
    pais = models.ForeignKey(
        Pais, blank=False, null=False, verbose_name='Pais')

    class Meta:
        verbose_name = u'Departameto'
        verbose_name_plural = u'Departamentos'

    def __unicode__(self):
        return self.nombre


class Provincia(models.Model):
    codigo = models.CharField(verbose_name='Codigo', max_length=6, blank=True)
    nombre = models.CharField(
        max_length=100, verbose_name='Nombre', null=False)
    departamento = models.ForeignKey(
        Departamento, blank=False, null=False, verbose_name='Departamento')

    class Meta:
        verbose_name = u'Provincia'
        verbose_name_plural = u'Provincias'

    def __unicode__(self):
        return self.nombre


class Distrito(models.Model):
    codigo = models.CharField(verbose_name='Codigo', max_length=6, blank=True)
    nombre = models.CharField(
        max_length=100, verbose_name='Nombre', null=False)
    provincia = models.ForeignKey(
        Provincia, blank=False, null=False, verbose_name='Provincia')

    class Meta:
        verbose_name = u'Distrito'
        verbose_name_plural = u'Distritos'

    def __unicode__(self):
        return self.nombre
