# coding=utf-8
import requests
from django.conf import settings
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import FormView, RedirectView, View
from django.views.generic.base import ContextMixin, TemplateView

from .forms import LoginForm


class MinsaLoginRequiredView(ContextMixin, View):
    login_url = settings.LOGIN_URL
    username = ''
    full_name = ''
    is_authenticated = False
    current_establishment = None
    require_establishment = True
    auth_establishments = []
    permissions = {}
    auth_unit_service = None
    auth_roles = None

    def __init__(self):

        super(MinsaLoginRequiredView, self).__init__()
        self.logout = False
        self.doesnt_need_role = False

    def dispatch(self, request, *args, **kwargs):
        auth_token = request.session.get('auth_token', None)

        if not auth_token:
            return HttpResponseRedirect(self.login_url)
        else:
            if not self.username:
                headers = {'Authorization': 'Token {}'.format(auth_token)}
                data = requests.get('{}api/v1/permisos/'.format(settings.URL_LOGIN_SERVER), headers=headers).json()
                if data.get('detail', ''):
                    request.session['auth_token'] = ''
                    return HttpResponseRedirect(self.login_url)

                self.username = data.get('username', '')
                self.full_name = data.get('full_name', '')
                self.name = data.get('name','')
                self.last_name = data.get('lastname_father','')
                self.auth_establishments = data.get('authorization', {}).get('establishments', [])
                self.permissions = data.get('authorization', {}).get('permissions', [])
                self.is_authenticated = True
                self.current_establishment = self.request.session.get('current_establishment', None)

                if self.doesnt_need_role:
                    pass
                elif self.auth_roles:

                    if True in [x in self.auth_roles for x in self.get_roles()]:
                        pass
                    else:
                        return HttpResponseRedirect(reverse('minsalogin:error403'))
                else:
                    if not self.logout:
                        return HttpResponseRedirect(reverse('minsalogin:error403'))
            if self.is_authenticated and self.require_establishment and not self.current_establishment:
                return HttpResponseRedirect(reverse('minsalogin:choose_establishment'))

        return super(MinsaLoginRequiredView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super(MinsaLoginRequiredView, self).get_context_data(**kwargs)
        user = {"username": self.username, "is_authenticated": self.is_authenticated, "full_name": self.full_name,
                "permissions": self.permissions, "auth_establishments": self.auth_establishments,
                "current_establishment": self.current_establishment}
        context['user'] = user
        return context

    def get_roles(self, unit_service=None):

        roles = []
        if self.current_establishment:
            if unit_service or self.auth_unit_service:
                roles = self.permissions.get(self.current_establishment, {}).get(
                    settings.APP_IDENTIFIER, {}).get(
                    unit_service if unit_service is not None else self.auth_unit_service)
            else:
                # perms = self.permissions.get(self.current_establishment).get(APP_IDENTIFIER)
                perms = self.permissions.get('estab:{}'.format(self.current_establishment)).get(settings.APP_IDENTIFIER)

                if perms:
                    x_roles_id = [x[1] for x in perms.items()]
                    for roles_id in x_roles_id:
                        for role_id in roles_id:
                            roles.append(role_id)
        else:
            all_establishments = list(set(self.permissions.keys()))
            us_roles = [(x.get(settings.APP_IDENTIFIER) if x.get(settings.APP_IDENTIFIER) is not None else {}) for x in
                        [self.permissions.get(e) for e in all_establishments]]
            try:
                us_roles = list(set(us_roles))
                us_roles.remove(None)
            except:
                pass
            if us_roles:
                if self.auth_unit_service:
                    x_roles = [x.get(self.auth_unit_service) for x in us_roles]
                    for roles_id in x_roles:
                        for role_id in roles_id:
                            roles.append(role_id)
                else:
                    x_roles = [[y for y in x.values()] for x in us_roles]
                    for x_roles_id in x_roles:
                        for roles_id in x_roles_id:
                            for role_id in roles_id:
                                roles.append(role_id)
        roles = list(set(roles))
        return list(set(roles))


class MinsaLoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('auth_token', ''):
            return HttpResponseRedirect('/')
        return super(MinsaLoginView, self).dispatch(request)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        payload = {'username': username, 'password': password}
        d = requests.post('{}auth/login/'.format(settings.URL_LOGIN_SERVER), payload).json()
        if d.get('auth_token'):
            self.request.session['auth_token'] = d.get('auth_token')
        else:
            return self.form_invalid(form)
        return super(MinsaLoginView, self).form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, login_error=True))

    def get_success_url(self):
        return '/escoger-establecimiento'
        # return '/'


class MinsaLogoutView(MinsaLoginRequiredView, RedirectView):
    require_establishment = False
    redirect_url = '/'

    def dispatch(self, request, *args, **kwargs):
        self.logout = True
        return super(MinsaLogoutView, self).dispatch(request)

    def get_redirect_url(self, **kwargs):
        self.username = ''
        self.current_establishment = None
        self.require_establishment = False
        self.auth_establishments = []
        headers = {'Authorization': 'Token {}'.format(self.request.session.get('auth_token'))}
        requests.post('{}auth/logout/'.format(settings.URL_LOGIN_SERVER), headers=headers)
        logout(self.request)
        self.request.session.flush()
        self.request.session['auth_token'] = ''
        self.is_authenticated = False
        return self.redirect_url


class MinsaLoginChooseEstablishment(MinsaLoginRequiredView, TemplateView):
    require_establishment = False
    template_name = 'perfiles/choose_establecimiento.html'

    def dispatch(self, request, *args, **kwargs):

        self.doesnt_need_role = True
        return super(MinsaLoginChooseEstablishment, self).dispatch(request)

    def get_context_data(self, **kwargs):

        context = super(MinsaLoginChooseEstablishment, self).get_context_data()
        establishments = self.auth_establishments
        context['establishments'] = establishments

        return context

    def post(self, request):

        establishment_code = self.request.POST.get('establishment', None)
        ruta = self.request.POST.get('action', None)

        if establishment_code:
            self.current_establishment = establishment_code
            self.request.session['current_establishment'] = establishment_code
            # self.request.session['establecimiento_id'] = establishment_code

        if ruta != '2':
            return HttpResponseRedirect(reverse('partos:home'))
        else:
            return HttpResponseRedirect(reverse('dashboard_home'))


class Error403(TemplateView):
    template_name = '403.html'
