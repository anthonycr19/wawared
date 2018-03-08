from django.conf.urls import patterns, url
from .views import cpt_search

urlpatterns = patterns(
    '',
    url(r'^buscar-cpt/$', cpt_search, name='api_search'),
)
