# -*- coding: utf-8 -*-
from django.db import models


class ServicioReniec(models.Model):
    namespace = models.CharField(verbose_name='NameSpace', max_length=250)
    urlwsdlservice = models.CharField(verbose_name='UrlWSLD', max_length=500)
    appservice = models.CharField(verbose_name='App', max_length=100)
    userservice = models.CharField(verbose_name='User', max_length=8)
    passservice = models.CharField(verbose_name='Password', max_length=500)

    class Meta:
        verbose_name = u'SERVICIO DNI RENIEC'
        verbose_name_plural = u'SERVICIO DNI RENIECS'

    def __unicode__(self):
        return self.urlwsdlservice
