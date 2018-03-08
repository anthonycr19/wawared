from django.conf.urls import patterns, url

from .views import (
    CitaCreateView, CitaUpdateView, CitaDeleteView, CitasCalendarView,
    CitasEventJsonView)

urlpatterns = patterns(
    '',
    # Admin
    url(
        r'^registrar/$',
        CitaCreateView.as_view(),
        name='register'),
    url(
        r'^(?P<id>\d+)/editar/$',
        CitaUpdateView.as_view(),
        name='edit'),
    url(
        r'^(?P<id>\d+)/eliminar/$',
        CitaDeleteView.as_view(),
        name='delete'),
    url(
        r'^calendario/$',
        CitasCalendarView.as_view(),
        name='calendar'),
    url(
        r'^eventos/$',
        CitasEventJsonView.as_view(),
        name='events')
)
