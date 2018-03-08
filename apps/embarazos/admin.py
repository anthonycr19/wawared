from django.contrib import admin

from .models import (
    Embarazo, Ecografia, UltimoEmbarazo, FichaViolenciaFamiliar, Bebe)


class EmbarazoAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'padre', 'numero_controles')


admin.site.register(Embarazo, EmbarazoAdmin)
admin.site.register(Ecografia)
admin.site.register(UltimoEmbarazo)
admin.site.register(FichaViolenciaFamiliar)
admin.site.register(Bebe)
