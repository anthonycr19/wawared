from ubigeo.models import Pais, Departamento, Provincia, Distrito
from django.contrib import admin


class PaisAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo')
    search_fields = ('nombre', 'codigo')


class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'pais')
    search_fields = ('nombre', 'pais__nombre')


class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'departamento')
    search_fields = ('nombre', 'departamento__nombre')


class DistritoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'provincia')
    search_fields = ('nombre', 'provincia__nombre')


admin.site.register(Pais, PaisAdmin)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Provincia, ProvinciaAdmin)
admin.site.register(Distrito, DistritoAdmin)
