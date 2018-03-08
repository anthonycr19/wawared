from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import CatalogoProcedimiento


@admin.register(CatalogoProcedimiento)
class CatalogoProcedimientoAdmin(ImportExportModelAdmin):
    list_display = ('denominacion_procedimientos', 'codigo_cpt')
    search_fields = ('codigo_cpt', 'denominacion_procedimientos')
