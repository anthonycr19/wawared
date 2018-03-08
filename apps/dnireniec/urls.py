from django.conf.urls import patterns, url

import views

urlpatterns = patterns(
    '',
    url(
        r'^consulta/(?P<num_dni>\d+)/',
        views.consultadni,
        name='search_dni')
)
