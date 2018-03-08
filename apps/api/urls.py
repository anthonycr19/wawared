from django.conf.urls import patterns, url, include

from .views import resources

res = patterns(
    '',
    url(r'^paciente/$', resources.PacienteView.as_view()),
    url(r'^paciente/(?P<tipodoc>\w+)/(?P<nrodoc>\d+)/$',
        resources.PacienteCiudadanoView.as_view(), name='search_paciente_tipo'),
    url(r'^paciente/(?P<dni>\d+)/$', resources.PacienteCiudadanoView.as_view(), name='search_paciente'),
)

urlpatterns = patterns(
    '',
    url(
        r'interoperabilidad/(?P<dni>\d+)/$',
        resources.PacienteDNIView.as_view()),
    url(
        r'^resources/',
        include(res, namespace='resources'))
)
