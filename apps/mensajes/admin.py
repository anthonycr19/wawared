from django.contrib import admin

from .models import *


class MensajesAdmin(admin.ModelAdmin):
    list_filter = ('tipo_mensaje', 'semana_mensaje',)


admin.site.register(Mensajes, MensajesAdmin)
