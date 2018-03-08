from django.contrib import admin
from models import ServicioReniec
from forms import ServiceReniecForm


class ServicioReniecAdmin(admin.ModelAdmin):
    form = ServiceReniecForm


admin.site.register(ServicioReniec, ServicioReniecAdmin)
