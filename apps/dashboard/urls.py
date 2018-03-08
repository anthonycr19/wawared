from django.conf.urls import patterns, url, include

import views

urlpatterns = patterns(
    '',
    url(r'^$', views.DashboardHomeView.as_view(), name='dashboard_home'),
    url(r'^paciente/', include('pacientes.urls', namespace='paciente')),
    url(r'^paciente/', include('embarazos.urls', namespace='embarazos')),
    url(r'^paciente/', include('controles.urls', namespace='controles')),
    url(
        r'^reportes-estadisticos/',
        include('indicadores.urls', namespace='indicadores')),
    url(r'^citas/', include('citas.urls', namespace='cita')),
    url(
        r'^establecimientos/',
        include('establecimientos.urls', namespace='establecimientos')),
)
