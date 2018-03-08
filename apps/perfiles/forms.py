# coding:utf-8
from __future__ import unicode_literals

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.conf import settings
from django.contrib.admin.widgets import FilteredSelectMultiple

from establecimientos.models import Establecimiento
from .models import UsuarioEstablecimiento


class EstablecimientoFilteredSelectMultiple(FilteredSelectMultiple):
    class Media:
        js = (
            "%s%s" % (settings.STATIC_URL, "admin/js/core.js"),
            "%s%s" % (settings.STATIC_URL, "admin/js/SelectBox.js"),
            "%s%s" % (settings.STATIC_URL, "admin/js/SelectFilter2.js"),
            "%s%s" % (settings.STATIC_URL, "js/ajax_establecimiento_list.js?ver=1.0.4"),
        )


class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def clean(self, value):
        return [val for val in value]


User = get_user_model()


class CustomUserForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            # User.objects.get(username=username)

            return username
        except User.DoesNotExist:
            raise forms.ValidationError(u'El usuario ingresado no existe')


class ChooseEstablecimientoForm(forms.Form):
    accion_field = forms.CharField(widget=forms.HiddenInput())
    establecimiento = forms.ModelChoiceField(queryset=Establecimiento.objects.none())

    def __init__(self, *args, **kwargs):
        super(ChooseEstablecimientoForm, self).__init__(*args, **kwargs)
        self.fields['establecimiento'].widget.attrs['class'] = 'form-control'

    def set_establecimientos(self, establecimientos):
        self.fields['establecimiento'].queryset = establecimientos


class ResetPasswordForm(forms.Form):
    username = forms.CharField(max_length=100)
    user = None

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            self.user = User.objects.get(username=username)
            if not self.user.email:
                raise forms.ValidationError(
                    'Este usuario no tiene un correo asignado, contacte con '
                    'el administrador')
            return username
        except User.DoesNotExist:
            raise forms.ValidationError('El usuario ingresado no existe')

    def get_user(self):
        return self.user


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        max_length=100, widget=forms.PasswordInput())
    new_password = forms.CharField(
        max_length=100, widget=forms.PasswordInput())
    user = None

    def clean_current_password(self):
        password = self.cleaned_data['current_password']
        access = authenticate(username=self.user.username, password=password)
        if access:
            return password
        else:
            raise forms.ValidationError('Contraseña incorrecta')

    def set_user(self, user):
        self.user = user


class UsuarioEstablecimientosForm(forms.ModelForm):
    establecimientos = CustomModelMultipleChoiceField(
        queryset=Establecimiento.objects.filter(id__in=(Establecimiento.objects.all().order_by('-id')[:20])),
        widget=EstablecimientoFilteredSelectMultiple('establecimentos', False))

    def __init__(self, *args, **kwargs):
        super(UsuarioEstablecimientosForm, self).__init__(*args, **kwargs)
        try:
            i = kwargs["instance"]
            usuarioestablecimiento = UsuarioEstablecimiento.objects.get(pk=i.pk)
            qs = usuarioestablecimiento.establecimientos.all()
            self.fields['establecimientos'].queryset = qs
        except:
            pass
