# Python imports


# Django imports
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

# Third party apps imports
from import_export.resources import ModelResource

# Local imports
from establecimientos.models import Establecimiento
from .models import UsuarioEstablecimiento, GroupRolMinsa


class UserResource(ModelResource):
    def before_import(self, dataset, dry_run, **kwargs):
        i = 0
        last = dataset.height - 1
        aux = None

        while i <= last:
            aux = list(dataset.lpop())
            aux[1] = make_password(aux[1])
            aux[8] = Establecimiento.objects.get(codigo=aux[8]).id
            dataset.rpush(tuple(aux))
            i += 1

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'groups', 'username', 'password', 'last_name', 'first_name',
            'email', 'type', 'celular', 'establecimiento', 'dni', 'his',
            'colegiatura',)
        exclude = (
            'date_joined', 'is_active', 'is_staff', 'is_superuser',
            'last_login', 'user_permissions',)


class UsuarioEstablecimientoResource(ModelResource):
    class Meta:
        model = UsuarioEstablecimiento
        fields = ('id', 'usuario', 'establecimientos',)
        exclude = ('created', 'modified',)


class GroupRolMinsaResource(ModelResource):
    class Meta:
        model = GroupRolMinsa
        fields = ('id', 'group', 'codigo_rol_minsa')
