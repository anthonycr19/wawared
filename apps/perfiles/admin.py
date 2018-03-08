# coding: utf-8
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from import_export.admin import ImportExportMixin, ImportExportModelAdmin

from .forms import CustomUserForm, UserCreationForm, UsuarioEstablecimientosForm
from .models import UsuarioEstablecimiento, User, GroupRolMinsa
from .resources import UserResource, UsuarioEstablecimientoResource, GroupRolMinsaResource


@admin.register(User)
class CustomUserAdmin(ImportExportMixin, UserAdmin):
    resource_class = UserResource
    form = CustomUserForm
    add_form = UserCreationForm
    raw_id_fields = ("establecimiento",)

    list_display = (
        'username', 'email', 'first_name', 'last_name', 'change_password_link',
        'is_admin', 'dni', 'his', 'colegiatura')
    list_filter = ('is_admin', 'type',)
    fieldsets = [
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': (
            'first_name', 'last_name', 'dni', 'celular', 'his', 'colegiatura',
            'establecimiento')}),
        ['Permissions', {'fields': ['type', 'is_admin', 'groups']}],
        ('Important Dates', {'fields': ('last_login',)}),
    ]

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')
        }),
    )

    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ('groups',)

    def change_password_link(self, obj):
        return u'<a href="{}">Cambiar contraseña</a>'.format(
            '/admin/perfiles/user/{}/password/'.format(obj.id))

    change_password_link.allow_tags = True


@admin.register(UsuarioEstablecimiento)
class UsuarioEstablecimintoAdmin(ImportExportModelAdmin):
    resource_class = UsuarioEstablecimientoResource
    form = UsuarioEstablecimientosForm
    list_display = ('usuario', 'created')

    search_fields = ('usuario__username', 'usuario__email', 'usuario__first_name', 'usuario__last_name')

    raw_id_fields = ("usuario",)


@admin.register(GroupRolMinsa)
class GroupRolMinsaAdmin(ImportExportModelAdmin):
    resource_class = GroupRolMinsaResource
