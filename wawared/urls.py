from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

handler403 = 'perfiles.views.handler_403'

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Api
    url(r'^api/', include('api.urls', namespace='api')),
    # CIE
    url(r'^cie/', include('cie.urls', namespace='cie')),
    # CPT
    url(r'^cpt/', include('cpt.urls', namespace='cpt')),
    # Admin
    url(r'^admin/', include(admin.site.urls)),
    # Perfiles
    url(r'^', include('perfiles.urls')),
    # Dahboard
    url(r'^', include('dashboard.urls')),
    # Ubigeo
    url('^ubigeo/', include('ubigeo.urls', namespace='ubigeo')),
    # Gestantes
    url(r'^hce/', include('gestantes.urls', namespace='gestantes')),
    url(r'session_security/', include('session_security.urls')),
    # Dnireniec
    url(r'^dnireniec/', include('dnireniec.urls', namespace='dnireniec')),
    # Partos
    url(r'^partos/', include('partos.urls', namespace='partos')),
    # Firma
    url(r'^firma/', include('firma.urls', namespace='firma')),
    # Puerperio
    url(r'^puerperio/', include('puerperio.urls', namespace='puerperio')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
