# coding:utf-8
from __future__ import unicode_literals

from common.views import LoginRequiredMixin
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import FormView, RedirectView
from establecimientos.models import Establecimiento
from perfiles.models import UsuarioEstablecimiento

import tasks
from backends import authenticate
from .forms import ChangePasswordForm, ChooseEstablecimientoForm, LoginForm, ResetPasswordForm


def handler_403(request):
    return render_to_response(
        'perfiles/403.html', context_instance=RequestContext(request))


class LoginView(FormView):
    template_name = 'dashboard/template_login/minsalogin/login.html'

    form_class = LoginForm

    def form_valid(self, form):
        data = form.cleaned_data
        username = data['username']
        password = data['password']
        # access = authenticate(username=username, password=password)
        access = authenticate(
            self.request, username=username, password=password)

        if access:
            auth_token = self.request.session.get('auth_token', None)
            login(self.request, access)
            self.request.session['auth_token'] = auth_token
        else:
            form.errors['password'] = ['Contraseña incorrecta']
            return self.form_invalid(form)
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        return reverse('choose_establecimiento')


class ChooseEstablecimientoView(LoginRequiredMixin, FormView):
    template_name = 'dashboard/template_login/minsalogin/choose_establishment.html'
    form_class = ChooseEstablecimientoForm
    ruta = None

    def get_form(self, form_class):
        form = super(ChooseEstablecimientoView, self).get_form(form_class)
        establecimientos = self.get_allowed_establecimientos()
        if not establecimientos.count():
            messages.error(
                self.request,
                'No tiene establecimientos asociados a su cuenta, '
                'contacte al adminsitrador')
        form.set_establecimientos(establecimientos)
        return form

    def form_valid(self, form):
        selected_establecimiento = form.cleaned_data['establecimiento']
        self.ruta = form.cleaned_data['accion_field']

        if self.establecimiento_belongs_to_user(selected_establecimiento):
            self.request.session[
                'modulo_citas'] = selected_establecimiento.modulo_citas
            self.request.session[
                'establecimiento_id'] = selected_establecimiento.id
        else:
            messages.error(
                self.request,
                'No tiene acceso al establecimiento seleccionado')
        return super(ChooseEstablecimientoView, self).form_valid(form)

    def get_success_url(self):

        if self.ruta == '3':
            self.request.session['modulo_control'] = False
            self.request.session['modulo_puerperio'] = True
            return reverse('puerperio:home')
        elif self.ruta == '2':
            self.request.session['modulo_control'] = False
            self.request.session['modulo_parto'] = True
            return reverse('partos:home')
        else:
            self.request.session['modulo_control'] = True
            self.request.session['modulo_parto'] = False
            return reverse('dashboard_home')

    def establecimiento_belongs_to_user(self, establecimiento):
        try:
            UsuarioEstablecimiento.objects.get(
                usuario=self.request.user, establecimientos=establecimiento)
            return True
        except UsuarioEstablecimiento.DoesNotExist:
            return False

    def get_allowed_establecimientos(self):
        try:
            ue = UsuarioEstablecimiento.objects.get(usuario=self.request.user)
            return ue.establecimientos.all()
        except UsuarioEstablecimiento.DoesNotExist:
            return Establecimiento.objects.none()


class LogoutView(RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        logout(self.request)
        return reverse('login')


class ResetPasswordView(FormView):
    template_name = 'perfiles/reset_password.html'
    form_class = ResetPasswordForm

    def form_valid(self, form):
        from uuid import uuid4
        new_password = uuid4().hex[:5]
        user = form.get_user()
        user.set_password(new_password)
        user.save()
        change_password_url = settings.DOMAIN + reverse('change_password')
        tasks.notify_password_reset.delay(
            user, new_password, change_password_url)
        messages.success(
            self.request,
            'Se envio un mensaje con su nueva contraseña a {}'.format(
                user.email))
        return super(ResetPasswordView, self).form_valid(form)

    def get_success_url(self):
        return reverse('login')


class ChangePasswordView(LoginRequiredMixin, FormView):
    template_name = 'perfiles/change_password.html'
    form_class = ChangePasswordForm

    def get_form(self, form_class):
        form = super(ChangePasswordView, self).get_form(form_class)
        form.set_user(self.request.user)
        return form

    def form_valid(self, form):
        data = form.cleaned_data
        new_password = data['new_password']
        print(new_password)
        self.request.user.set_password(new_password)
        self.request.user.save()
        messages.success(self.request, 'Contraseña cambiada')
        return super(ChangePasswordView, self).form_valid(form)

    def get_success_url(self):
        return reverse('dashboard_home')

    def get_context_data(self, **kwargs):
        context = super(ChangePasswordView, self).get_context_data(**kwargs)

        if self.request.session.get('establecimiento_id'):
            establecimiento_actual = Establecimiento.objects.get(
                id=self.request.session['establecimiento_id'])

            if 'modulo_control' in self.request.session:
                modulo_control = self.request.session['modulo_control']
            else:
                modulo_control = True

            if 'modulo_citas' in self.request.session:
                modulo_citas = self.request.session['modulo_citas']
            else:
                modulo_citas = False

            context.update({
                'establecimiento_actual': establecimiento_actual,
                'modulo_control': modulo_control,
                'modulo_citas': modulo_citas
            })
        else:
            context.update({
                'modulo_citas': True
            })

        return context
