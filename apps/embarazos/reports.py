from django.conf import settings
from common.util import BaseJasperReport


class FichaTamizajeReport(BaseJasperReport):
    report_name = 'ficha_tamizaje'

    def __init__(self, embarazo):
        self.embarazo = embarazo
        self.filename = 'ficha_tamizaje_{}_{}'.format(
            embarazo.paciente.tipo_documento.upper(),
            embarazo.paciente.numero_documento
        )
        super(FichaTamizajeReport, self).__init__()

    def get_params(self):
        logo = self.embarazo.establecimiento.logo
        logo_path = settings.MEDIA_ROOT + '/' + logo.name if logo.name else ''
        logo_minsa = '{0}/static/img/logo_minsa.png'.format(settings.DOMAIN)

        return {
            'embarazo_id': str(self.embarazo.id),
            'logo': logo_path or 'not',
            'logo_minsa': logo_minsa
        }


class TamizajeDepresionReport(BaseJasperReport):
    report_name = 'tamizaje_depresion'

    def __init__(self, embarazo):
        self.embarazo = embarazo
        self.filename = 'tamizaje_depresion_{}_{}'.format(
            embarazo.paciente.tipo_documento.upper(),
            embarazo.paciente.numero_documento
        )
        super(TamizajeDepresionReport, self).__init__()

    def get_params(self):
        return {
            'embarazo_id': str(self.embarazo.id)
        }
