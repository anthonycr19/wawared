from django.contrib import admin

from .models import *


class RelacionParentescoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'solo_femenino')
    list_editable = ('solo_femenino',)


class HistoriaClinicaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'establecimiento', 'paciente')


class PacienteAdmin(admin.ModelAdmin):
    list_filter = ('tipo_documento',)


admin.site.register(Paciente, PacienteAdmin)
admin.site.register(AntecedenteGinecologico)
admin.site.register(AntecedenteFamiliar)
admin.site.register(AntecedenteMedico)
admin.site.register(AntecedenteObstetrico)
admin.site.register(Estudio)
admin.site.register(Etnia)
admin.site.register(Ocupacion)
admin.site.register(RelacionParentesco, RelacionParentescoAdmin)
admin.site.register(Vacuna)
admin.site.register(HistoriaClinica, HistoriaClinicaAdmin)
