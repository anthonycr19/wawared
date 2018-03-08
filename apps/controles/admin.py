from django.contrib import admin

from .models import (
    Control, Diagnostico, ExamenFisico, Laboratorio, Sintoma,
    DiagnosticoDetalle, ExamenLaboratorio)


class ExamenLaboratorioAdmin(admin.ModelAdmin):
    list_display = ('nombre',)


admin.site.register(Control)
admin.site.register(Diagnostico)
admin.site.register(ExamenFisico)
admin.site.register(Laboratorio)
admin.site.register(Sintoma)
admin.site.register(DiagnosticoDetalle)
admin.site.register(ExamenLaboratorio, ExamenLaboratorioAdmin)
