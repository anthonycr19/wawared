from django.conf.urls import patterns, url

import views

urlpatterns = patterns(
    '',
    url(
        r'^departamentos/(?P<id>\d+)/',
        views.departamentos,
        name='departamentos'),
    url(
        r'^provincias/(?P<id>\d+)/',
        views.provincias,
        name='provincias'),
    url(
        r'^distritos/(?P<id>\d+)/',
        views.distritos,
        name='distritos'),
)
