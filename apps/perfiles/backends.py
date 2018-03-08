import requests
from django.conf import settings
from establecimientos.models import Establecimiento

from settings.base import URL_LOGIN_SERVER
from .models import GroupRolMinsa, User, UsuarioEstablecimiento


def authenticate(request, username=None, password=None):
    payload = {'username': username, 'password': password}

    try:
        auth_token = requests.post('{}auth/login/'.format(URL_LOGIN_SERVER), payload).json()

        if auth_token.get('auth_token'):
            headers = {'Authorization': 'Token {}'.format(auth_token.get('auth_token'))}
            data = requests.get('{}api/v1/permisos/'.format(URL_LOGIN_SERVER), headers=headers).json()
            user = get_user(username=username)

            if user is None:
                user = User()

            user.username = data.get('username', '')
            user.first_name = data.get('name', '')
            user.last_name = '{} {}'.format(data.get('lastname_father', ''), data.get('lastname_mother', ''))
            user.dni = data.get('username', '')
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            user.set_password(password)
            user.save()

            permissions = data['authorization']['permissions']
            permisos_all_dic = {}
            lista_estab = []

            for estab_rol in permissions.keys():

                if permissions[estab_rol].has_key(settings.APP_IDENTIFIER):

                    unidad_servicio = permissions[estab_rol][settings.APP_IDENTIFIER]
                    for unidad in unidad_servicio:
                        for rol in unidad_servicio[unidad]:
                            if not permisos_all_dic.has_key(rol):
                                permisos_all_dic[rol] = ''

                    codigo_renaes = estab_rol.replace("estab:", "")
                    estab = get_establecimiento(codigo_renaes=codigo_renaes)
                    if not estab is None:
                        lista_estab.append(estab)

            if len(permisos_all_dic) > 0:
                lista_group = []
                index_rol = 0

                for rol in permisos_all_dic.keys():

                    group_object = get_group(codigo_rol_minsa=rol)

                    if not group_object is None:
                        lista_group.append(group_object)
                        index_rol += 1

                user.groups = lista_group
                user.save()

            if UsuarioEstablecimiento.objects.filter(usuario=user).count() == 0:
                usua_estab = UsuarioEstablecimiento(usuario=user)
                usua_estab.save()
            else:
                usua_estab = UsuarioEstablecimiento.objects.filter(usuario=user).last()

            if len(lista_estab) > 0:
                user.establecimiento = lista_estab[0]
                user.save()

            usua_estab.establecimientos = lista_estab

            usua_estab.save()

            request.session['auth_token'] = auth_token.get('auth_token')

            return user
    except Exception as e:
        print(e)


def get_user(username=None):
    try:
        user = User.objects.get(username=username)
        return user
    except Exception as e:
        return None


def get_group(codigo_rol_minsa=None):
    try:
        group_rol_minsa = GroupRolMinsa.objects.get(codigo_rol_minsa=codigo_rol_minsa)
        return group_rol_minsa.group
    except Exception as e:
        return None


def get_establecimiento(codigo_renaes=None):
    try:
        establecimiento = Establecimiento.objects.get(codigo=codigo_renaes)
        return establecimiento
    except Exception as e:
        return None
