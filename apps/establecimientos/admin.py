from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import Establecimiento, Microred, Red, Diresa, DownloadReport
from .resources import (
    DiresaResource, RedResource, MicroredResource, EstablecimientoResource, )


@admin.register(Red)
class RedAdmin(ImportExportModelAdmin):
    resource_class = RedResource
    list_display = ('nombre', 'diresa', 'estado')


@admin.register(Microred)
class MicroredAdmin(ImportExportModelAdmin):
    resource_class = MicroredResource
    list_display = ('nombre', 'red', 'estado')


@admin.register(Establecimiento)
class EstablecimientoAdmin(ImportExportModelAdmin):
    resource_class = EstablecimientoResource
    list_display = (
        'nombre', 'codigo', 'codigo_his', 'microred', 'red', 'diresa', 'lote',
        'descripcion', 'telefono')
    search_fields = ('nombre', 'codigo', 'diresa__nombre', 'red__nombre', 'microred__nombre')


@admin.register(Diresa)
class DiresaAdmin(ImportExportModelAdmin):
    resource_class = DiresaResource


admin.site.register(DownloadReport)
