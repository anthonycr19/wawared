# coding: utf-8
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

User = get_user_model()


def create_user(
    username='test', email='test@test.com', password='test',
    permissions=None):
    user = User.objects.create(
        username=username, email=email, password=password)
    if permissions and isinstance(permissions, (tuple, list)):
        for perm_name in permissions:
            if '.' not in perm_name:
                raise ValueError('permission name format incorrect')
            app_label, codename = perm_name.split('.')
            _perm = Permission.objects.get(
                content_type__app_label=app_label, codename=codename)
            user.user_permissions.add(_perm)
    return user
