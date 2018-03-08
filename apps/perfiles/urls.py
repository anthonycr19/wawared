from django.conf.urls import patterns, url

import views

urlpatterns = patterns(
    '',
    url(
        r'^ingresar/$',
        views.LoginView.as_view(),
        name='login'),
    url(
        r'^escoger-establecimiento/$',
        views.ChooseEstablecimientoView.as_view(),
        name='choose_establecimiento'),
    url(
        r'^resetear-clave/$',
        views.ResetPasswordView.as_view(),
        name='reset_password'),
    url(
        r'^cambiar-clave/$',
        views.ChangePasswordView.as_view(),
        name='change_password'),
    url(
        r'^salir/$',
        views.LogoutView.as_view(),
        name='logout'),
)
