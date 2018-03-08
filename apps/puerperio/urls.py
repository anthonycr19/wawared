from django.conf.urls import patterns, url, include

import views

reports = patterns(
    '',
    url(r'^epicrisis/(?P<egreso_gestante_id>\d+)/$',
        views.EpicrisisReportView.as_view(), name='epicrisis')
)

urlpatterns = patterns(
    '',
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^paciente/buscar/$',
        views.PPacienteSearchView.as_view(), name='paciente_search'),
    url(r'^resumen/(?P<terminacion_embarazo_id>\d+)/$',
        views.ResumeView.as_view(), name='resume'),
    url(r'^reportes/', include(reports, namespace='reports')),
    url(r'^(?P<terminacion_embarazo_id>\d+)/monitoreo/$',
        views.MonitoreoView.as_view(), name='monitoreo'),
    url(r'^(?P<terminacion_embarazo_id>\d+)/monitoreo/medicion/(?P<medicion_id>\d+)/$',
        views.MonitoreoMedicionUpdateView.as_view(
        ), name='monitoreo_medicion'),
    url(r'^terminacion_embarazo/(?P<terminacion_embarazo_id>\d+)/egreso/redirect/$',
        views.EgresoGestanteView.as_view(), name='egreso_gestante'),
    url(r'^terminacion_embarazo/(?P<terminacion_embarazo_id>\d+)/registrar-egreso/$',
        views.EgresoGestanteCreateView.as_view(
        ), name='egreso_gestante_create'),
    url(r'^terminacion_embarazo/(?P<terminacion_embarazo_id>\d+)/egreso/$',
        views.EgresoGestanteUpdateView.as_view(), name='egreso_gestante_edit'),
    url(r'^(?P<terminacion_embarazo_id>\d+)/recien-nacido/create/$',
        views.RecienNacidoCreateView.as_view(), name='recien_nacido_create'),
    url(r'^(?P<terminacion_embarazo_id>\d+)/recien-nacido/(?P<recien_nacido_id>\d+)/edit/',
        views.RecienNacidoUpdateView.as_view(), name='recien_nacido_edit'),
    url(r'^(?P<terminacion_embarazo_id>\d+)/cierre-puerpera/$',
        views.TerminacionPuerperaView.as_view(), name='cierre_puerpera'),
)
