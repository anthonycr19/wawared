# coding:utf-8
from __future__ import unicode_literals
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager, Group)
from django.core.validators import RegexValidator

from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, contrasena_gestante='',
                    first_name='', last_name='', type=''):

        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.username = username
        user.set_password(password)
        if contrasena_gestante != '':
            user.contrasena_gestante = contrasena_gestante
        if first_name != '':
            user.first_name = first_name
        if last_name != '':
            user.last_name = last_name
        if type != '':
            user.type = type
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

    MEDICO = 'medico'
    LICENCIADO = 'licenciado'
    OBSERVADOR = 'observador'
    ESTADISTICA = 'estadistica'
    GESTANTE = 'gestante'

    TYPE_CHOICES = (
        (MEDICO, u'Médico'),
        (LICENCIADO, 'Obstetra'),
        (OBSERVADOR, 'Observador'),
        (ESTADISTICA, u'Estadística'),
        (GESTANTE, 'Gestante')
    )

    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contrasena_gestante = models.CharField(editable=False, blank=True, max_length=5)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    type = models.CharField('Tipo de usuario', max_length=100, default=OBSERVADOR,
                            choices=TYPE_CHOICES)
    servicio = models.CharField('Servicio', max_length=20, null=True, blank=True)

    objects = CustomUserManager()

    establecimiento = models.ForeignKey('establecimientos.Establecimiento', null=True,
                                        verbose_name='Establecimiento origen', blank=True)
    dni = models.CharField('DNI', max_length=8, null=True, blank=True)
    his = models.CharField('HIS', max_length=13, null=True, blank=True)
    colegiatura = models.CharField(
        'Colegiatura', max_length=20, null=True, validators=[RegexValidator(
            regex='^\d+$', message=u'Se deben ingresar valores numéricos')],
        blank=True)
    celular = models.CharField('Celular', max_length=15, null=True, blank=True)

    @property
    def is_staff(self):
        return self.is_admin

    def __unicode__(self):
        return self.username

    class Meta:
        verbose_name = 'Usuario de sistema'
        verbose_name_plural = 'Usuarios del sistema'

    def get_full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.username


class UsuarioEstablecimiento(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuario', unique=True)
    establecimientos = models.ManyToManyField('establecimientos.Establecimiento', blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = 'Usuario Establecimiento'
        verbose_name_plural = 'Usuarios de Establecimiento'

    def __unicode__(self):
        return self.usuario.username


class GroupRolMinsa(models.Model):
    group = models.ForeignKey(Group, verbose_name='Grupo del Sistema')
    codigo_rol_minsa = models.CharField('Rol Minsa login', max_length=3)

    class Meta:
        verbose_name = 'Grupo_Roles_Minsa'
        verbose_name_plural = 'Grupos_Roles_Minsa'
