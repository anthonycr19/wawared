# coding: utf-8
from __future__ import unicode_literals

from common.util import BaseJasperReport


class PartosControlesPrenatalReport(BaseJasperReport):
    report_name = 'partos_controles_prenatal'
    embarazo = None

    def __init__(self, embarazo):
        self.embarazo = embarazo
        self.filename = 'partos_controles_prenatal{}_{}'.format(
            embarazo.paciente.tipo_documento.upper(), embarazo.paciente.numero_documento
        )
        super(PartosControlesPrenatalReport, self).__init__()

    def get_params(self):
        return {
            'embarazo_id': self.embarazo.id
        }


class HojaMonitoreoMaternoFetalReport(BaseJasperReport):
    report_name = 'hoja_monitoreo_materno_fetal'

    def __init__(self, partograma):
        self.partograma = partograma
        self.filename = 'hoja_monitoreo_materno_fetal_{}_{}'.format(
            partograma.paciente.tipo_documento.upper(), partograma.paciente.numero_documento
        )
        super(HojaMonitoreoMaternoFetalReport, self).__init__()

    def get_params(self):
        return {
            'partograma_id': str(self.partograma.id)
        }


class PartosHistoriaClinicaReport(BaseJasperReport):
    report_name = 'partos_historia_clinica'
    establecimiento = None
    embarazo = None

    def __init__(self, embarazo):
        self.embarazo = embarazo
        self.filename = 'partos_historia_clinica_{}_{}'.format(
            embarazo.paciente.tipo_documento.upper(), embarazo.paciente.numero_documento
        )
        super(PartosHistoriaClinicaReport, self).__init__()

    def get_params(self):
        return {
            'embarazo_id': self.embarazo.id
        }
