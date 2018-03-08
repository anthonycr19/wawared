from django.conf.urls import patterns, url, include

import views

reports = patterns(
    '',
    url(r'sien/$', views.SIENReportView.as_view(), name='sien'),
    url(
        r'reporte-global/$',
        views.GlobalReportView.as_view(),
        name='reporte_global'),
    url(
        r'reporte-global-parto/$',
        views.GlobalReportPartoView.as_view(),
        name='reporte_global_parto'),
    url(
        r'reporte-global-puerperio/$',
        views.GlobalReportPuerperioView.as_view(),
        name='reporte_global_puerperio'),
    url(
        r'libro-de-registro-diario-de-gestantes/$',
        views.LibroRegistroDiarioSeguimientoGestantesReportView.as_view(),
        name='libro_registro_diario_gestantes'),
    url(
        r'descargar-reporte/(?P<report_id>\d+)/$',
        views.DownloadReportFileView.as_view(),
        name='download_report')
)

urlpatterns = patterns(
    '',
    url(r'^reportes/', include(reports, namespace='reports')),
    url(r'^get_json_establecimientos/(?P<query>[\w-]+)/$', views.get_json_establecimientos,
        name='get_json_establecimientos'),
    url(r'^buscar-establecimiento/$',
        views.establecimiento_search, name='establecimiento_search'),
)
