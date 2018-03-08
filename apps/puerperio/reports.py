# coding: utf-8
from __future__ import unicode_literals

from common.util import BaseJasperReport


class EpicrisisReport(BaseJasperReport):

	report_name = 'epicrisis_gestante'

	def __init__(self, egreso):
		self.egreso = egreso
		self.filename = 'epicrisis_{}'.format(egreso.paciente.numero_documento)
		super(EpicrisisReport, self).__init__()

	def get_params(self):
		return {
			'egreso_gestante_id': self.egreso.id
		}
