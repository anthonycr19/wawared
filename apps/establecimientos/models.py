# encoding:utf-8
from django.conf import settings

from django.db import models


class Diresa(models.Model):
    nombre = models.CharField(u'Nombre', max_length=100)
    logo = models.ImageField(upload_to='diresas/logos/', null=True, blank=True)
    codigo = models.CharField(blank=True, max_length=3, null=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return self.nombre


class Red(models.Model):
    diresa = models.ForeignKey('Diresa', blank=True, null=True)
    nombre = models.CharField(u'Nombre', max_length=100, null=False)
    estado = models.BooleanField(u'Estado', default=True)
    logo = models.ImageField(upload_to='redes/logos/', null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = u'Red'
        verbose_name_plural = u'Redes'

    def __unicode__(self):
        return self.nombre


class Microred(models.Model):
    red = models.ForeignKey('Red', blank=True, null=True)
    nombre = models.CharField(u'Nombre', max_length=100)
    numero = models.IntegerField(blank=True, null=True)
    estado = models.BooleanField(u'Estado', default=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = u'Micro Red'
        verbose_name_plural = u'Micro Redes'

    def __unicode__(self):
        return self.nombre


class Establecimiento(models.Model):
    diresa = models.ForeignKey('Diresa', blank=True, null=True, editable=False)
    red = models.ForeignKey('Red', blank=True, null=True)
    microred = models.ForeignKey('Microred', blank=True, null=True)
    codigo = models.CharField(u'Código Renaes', max_length=50)
    disa = models.CharField('Disa', max_length=50, blank=True, null=True)
    logo = models.ImageField(
        upload_to='establecimientos/logos/', null=True, blank=True)
    telefono = models.CharField(u'Teléfono', max_length=20, blank=True)
    nombre = models.CharField(u'Nombre', max_length=150)
    descripcion = models.TextField(
        u'Descripción', max_length=150, blank=True, null=True)
    codigo_his = models.CharField(
        u'Código HIS', max_length=10, null=True, blank=True)
    lote = models.SmallIntegerField(null=False, default=0)
    is_sistema_externo_admision = models.NullBooleanField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    modulo_parto = models.BooleanField(u'Parto', default=False)
    modulo_citas = models.BooleanField(u'Citas', default=False)
    fuas_trama = models.NullBooleanField('Habilitada Trma SIS')
    fuas_numinicial = models.IntegerField('Numero de FUA rango inicial SIS', null=False, default=0)
    fuas_numfinal = models.IntegerField('NUmero de FUA rango Final SIS', null=False, default=0)
    fuas_incremento = models.IntegerField(null=False, default=0)
    fuas_udr = models.CharField('UDR SIS', max_length=3, blank=True, null=True)
    fuas_categoria = models.CharField('Categoria SIS', max_length=2, blank=True, null=True)
    fuas_nivel = models.CharField('Nivel SIS', max_length=1, blank=True, null=True)
    fuas_codconvenido = models.CharField('Codigo Convenio SIS', max_length=1, blank=True, null=True)
    fuas_disa = models.CharField('DISA SIS', max_length=3, blank=True, null=True)

    class Meta:
        verbose_name = u'Establecimiento'
        verbose_name_plural = u'Establecimientos'
        permissions = (
            ('download_reporte_global', 'Descargar reporte global'),
            ('download_reporte_sien', 'Descargar reporte SIEN'),
            ('download_reporte_registro_diario_gestaciones',
             'Descargar registro diario de gestaciones'),
        )

    def save(
        self, force_insert=False, force_update=False, using=None,
        update_fields=None):
        if self.red:
            self.diresa = self.red.diresa
        super(Establecimiento, self).save(
            force_insert, force_update, using, update_fields)

    def __unicode__(self):
        return "%s - %s - %s" % (self.codigo, self.nombre, self.diresa.nombre)


class DownloadReport(models.Model):
    file = models.FileField(
        upload_to='reports/%Y/%m/%d/', null=True, blank=True)
    filename = models.CharField(max_length=100)
    content_type = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='in process')

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='download_report')
    created = models.DateTimeField(auto_now_add=True, editable=False)
