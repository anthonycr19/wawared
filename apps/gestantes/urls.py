from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout

from .views import ReportesTemplateView, generar_reporte

# Create your views here.
urlpatterns = patterns(
    '',
    url(
        r'^$',
        login,
        name='login',
        kwargs={'template_name': 'gestantes/login.html'}
    ),
    url(
        r'^logout/$',
        logout,
        name='hce_logout',
        kwargs={'next_page': '/hce/'}
    ),
    url(
        r'^reportes/$',
        # r'^reportes/(?P<paciente_id>\d+)/$',
        ReportesTemplateView.as_view(),
        name='reportes'
    ),
    url(
        r'^wasd/$',
        generar_reporte,
        name='reporte'
    ),
)
