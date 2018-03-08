from django.contrib import admin
from .models import Cita


class CitaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'establecimiento', 'fecha', 'is_wawared',)
    list_editable = ('fecha', 'establecimiento',)
    search_fields = ('establecimiento__nombre', 'fecha',)


admin.site.register(Cita, CitaAdmin)
