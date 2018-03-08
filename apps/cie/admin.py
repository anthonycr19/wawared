from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import ICD10Base
from .resources import ICD10BaseResource


@admin.register(ICD10Base)
class ICD10BaseAdmin(ImportExportModelAdmin):
    resource_class = ICD10BaseResource
    list_display = ('nombre', 'nombre_mostrar', 'codigo')
    search_fields = ('codigo', 'nombre')
