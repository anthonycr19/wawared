from django.conf.urls import patterns, url
from .views import cie_search

urlpatterns = patterns(
    '',
    url(r'^buscar-cie/$', cie_search, name='api_search'),
)
