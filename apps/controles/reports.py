# coding: utf-8
import xlsxwriter

from datetime import datetime
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from django.conf import settings
from django.http import HttpResponse, Http404

from common.util import BaseJasperReport
from controles.models import Laboratorio, ExamenFisico, ExamenFisicoFetal
from firma.models import Document


class HistoriaClinicaReport(BaseJasperReport):
    report_name = 'historia_clinica'

    def __init__(self, control):
        self.control = control
        self.filename = 'historia_clinica_{}_{}'.format(
            self.control.paciente.tipo_documento.upper(),
            self.control.paciente.numero_documento)
        super(HistoriaClinicaReport, self).__init__()

    def get_params(self):

        ganancia_peso = self.control.embarazo.chart_ganancia_peso_materno
        if ganancia_peso.name:
            ganancia_peso_path = ''.join(['', '{0}/media/{1}'.format(settings.DOMAIN, ganancia_peso.name)])
        else:
            ganancia_peso_path = ''
        altura_uterina = self.control.embarazo.chart_altura_uterina
        if altura_uterina.name:
            altura_uterina_path = ''.join(['', '{0}/media/{1}'.format(settings.DOMAIN, altura_uterina.name)])
        else:
            altura_uterina_path = ''

        logo_minsa = '{0}/static/img/logo_minsa.png'.format(settings.DOMAIN)

        result = {
            'paciente_id': str(self.control.paciente.id),
            'control_id': str(self.control.id),
            'ganancia_peso_chart': ganancia_peso_path,
            'altura_uterina_chart': altura_uterina_path,
            'logo_minsa': logo_minsa
        }

        return result


class SolicitudExamenesClinicosReport(BaseJasperReport):
    report_name = 'solicitud_examenes_clinicos'

    def __init__(self, control):
        self.control = control
        self.filename = 'solicitud_examenes_clinicos_{}_{}'.format(
            control.paciente.tipo_documento.upper(),
            control.paciente.numero_documento
        )
        super(SolicitudExamenesClinicosReport, self).__init__()

    def get_params(self):
        logo = self.control.establecimiento.logo
        logo_path = settings.MEDIA_ROOT + '/' + logo.name if logo.name else ''
        logo_minsa = '{0}/static/img/logo_minsa.png'.format(settings.DOMAIN)

        return {
            'control_id': str(self.control.id),
            'establecimiento_logo': logo_path or 'not',
            'logo_minsa': logo_minsa
        }


class PlanPartoReport(BaseJasperReport):
    report_name = 'plan_parto'

    def __init__(self, control):
        self.control = control
        self.filename = 'plan_parto_{}_{}'.format(
            control.paciente.tipo_documento.upper(),
            control.paciente.numero_documento
        )
        super(PlanPartoReport, self).__init__()

    def get_params(self):
        logo_minsa = '{0}/static/img/logo_minsa.png'.format(settings.DOMAIN)

        return {
            'control_id': str(self.control.id),
            'logo_minsa': logo_minsa
        }


class TarjetaSeguimientoReport(BaseJasperReport):
    report_name = 'tarjeta_seguimiento'

    def __init__(self, control):
        self.control = control
        self.filename = 'tarjeta_seguimiento_{}_{}'.format(
            control.paciente.tipo_documento.upper(),
            control.paciente.numero_documento
        )
        super(TarjetaSeguimientoReport, self).__init__()

    def get_params(self):
        logo = self.control.establecimiento.logo
        logo_path = settings.MEDIA_ROOT + '/' + logo.name if logo.name else ''
        logo_minsa = '{0}/static/img/logo_minsa.png'.format(settings.DOMAIN)

        return {
            'control_id': str(self.control.id),
            'establecimiento_logo': logo_path or 'not',
            'logo_minsa': logo_minsa
        }


class RecetaUnicaEstandarizadaReport(BaseJasperReport):
    report_name = 'receta_unica_estandarizada'

    def __init__(self, control):
        self.control = control
        self.filename = 'receta_unica_estandarizada_{}_{}'.format(
            control.paciente.tipo_documento.upper(),
            control.paciente.numero_documento
        )
        super(RecetaUnicaEstandarizadaReport, self).__init__()

    def get_params(self):
        logo = self.control.establecimiento.logo
        logo_path = settings.MEDIA_ROOT + '/' + logo.name if logo.name else ''
        logo_minsa = '{0}/static/img/logo_minsa.png'.format(settings.DOMAIN)

        return {
            'control_id': str(self.control.id),
            'establecimiento_logo': logo_path or 'not',
            'logo_minsa': logo_minsa
        }


class RecetaUnicaFlujoVaginalReport(BaseJasperReport):
    report_name = 'receta_unica_flujo_vaginal'

    def __init__(self, control):
        self.control = control
        self.filename = 'receta_unica_flujo_vaginal_{}_{}'.format(
            control.paciente.tipo_documento.upper(),
            control.paciente.numero_documento
        )
        super(RecetaUnicaFlujoVaginalReport, self).__init__()

    def get_params(self):
        logo = self.control.establecimiento.logo
        logo_path = settings.MEDIA_ROOT + '/' + logo.name if logo.name else ''
        logo_minsa = '{0}/static/img/logo_minsa.png'.format(settings.DOMAIN)

        return {
            'control_id': str(self.control.id),
            'establecimiento_logo': logo_path or 'not',
            'logo_minsa': logo_minsa
        }


class RecetaUnicaPruebaRapidaReport(BaseJasperReport):
    report_name = 'receta_unica_prueba_rapida'

    def __init__(self, control):
        self.control = control
        self.filename = 'receta_unica_prueba_rapida_{}_{}'.format(
            control.paciente.tipo_documento.upper(),
            control.paciente.numero_documento
        )
        super(RecetaUnicaPruebaRapidaReport, self).__init__()

    def get_params(self):
        logo = self.control.establecimiento.logo
        logo_path = settings.MEDIA_ROOT + '/' + logo.name if logo.name else ''
        logo_minsa = '{0}/static/img/logo_minsa.png'.format(settings.DOMAIN)

        return {
            'control_id': str(self.control.id),
            'establecimiento_logo': logo_path or 'not',
            'logo_minsa': logo_minsa
        }


class FormatoUnicoAtencionReport(BaseJasperReport):
    report_name = 'formato_unico_atencion'

    def __init__(self, control):
        self.control = control
        self.filename = 'formato_unico_atencion_{}_{}'.format(
            control.paciente.tipo_documento.upper(),
            control.paciente.numero_documento
        )
        super(FormatoUnicoAtencionReport, self).__init__()

    def get_params(self):
        logo_minsa = '{0}/static/img/logo_minsa.png'.format(settings.DOMAIN)

        return {
            'control_id': str(self.control.id),
            'logo_minsa': logo_minsa
        }


class HojaReferenciaReport(BaseJasperReport):
    report_name = 'hoja_referencia'

    def __init__(self, control):
        self.control = control
        self.filename = 'hoja_referencia_{}_{}'.format(
            control.paciente.tipo_documento.upper(),
            control.paciente.numero_documento
        )
        super(HojaReferenciaReport, self).__init__()

    def get_params(self):
        logo_minsa = '{0}/static/img/logo_minsa.png'.format(settings.DOMAIN)

        return {
            'control_id': str(self.control.id),
            'examenes_auxiliares': self._get_examenes_auxiliares(),
            'examenes_fisicos': self._get_examenes_fisicos(),
            'logo_minsa': logo_minsa
        }

    def _get_examenes_fisicos(self):
        if hasattr(self.control, 'examen_fisico') and \
            self.control.examen_fisico:
            ef = self.control.examen_fisico
            exams = []
            if ef.piel_y_mucosas == ExamenFisico.PATOLOGICO:
                exams.append('Piel y mucosas')
            if ef.mamas == ExamenFisico.PATOLOGICO:
                exams.append('Mamas')
            if ef.respiratorio == ExamenFisico.PATOLOGICO:
                exams.append('Respiratorio')
            if ef.cardiovascular == ExamenFisico.PATOLOGICO:
                exams.append('Cardiovascular')
            if ef.odontologico == ExamenFisico.PATOLOGICO:
                exams.append('Odontologico')
            if ef.abdomen == ExamenFisico.PATOLOGICO:
                exams.append('Abdomen')
            if ef.urinario == ExamenFisico.PATOLOGICO:
                exams.append('Urinario')
            if ef.neurologico == ExamenFisico.PATOLOGICO:
                exams.append('Neurologico')
            return ', '.join(exams)
        return ''

    def _get_examenes_auxiliares(self):
        if hasattr(self.control, 'laboratorio') and self.control.laboratorio:
            lab = self.control.laboratorio
            exams = []
            if lab.rapida_hemoglobina:
                exams.append(
                    'Rapida hemoglobina: {}'.format(
                        lab.rapida_hemoglobina_resultado))
            if lab.hemoglobina_1:
                exams.append(
                    'Hemoglobina 1: {}'.format(lab.hemoglobina_1_resultado))
            if lab.hemoglobina_2:
                exams.append(
                    'Hemoglobina 2: {}'.format(lab.hemoglobina_2_resultado))
            if lab.hemoglobina_alta:
                exams.append(
                    'Hemoglobina al alta: {}'.format(
                        lab.hemoglobina_alta_resultado))
            if lab.glicemia_1 != Laboratorio.NO_SE_HIZO:
                exams.append('Glicemia 1: {}'.format(lab.glicemia_1))
            if lab.glicemia_2 != Laboratorio.NO_SE_HIZO:
                exams.append('Glicemia 2: {}'.format(lab.glicemia_2))
            if lab.tolerancia_glucosa != Laboratorio.NO_APLICA:
                exams.append(
                    'Tolerancia Glucosa: {}'.format(lab.tolerancia_glucosa))
            if lab.vdrl_rp_1 not in \
                (Laboratorio.NO_APLICA, Laboratorio.NO_SE_HIZO):
                exams.append('VDRL 1: {}'.format(lab.vdrl_rp_1))
            if lab.vdrl_rp_2 not in \
                (Laboratorio.NO_APLICA, Laboratorio.NO_SE_HIZO):
                exams.append('VDRL 2: {}'.format(lab.vdrl_rp_2))
            if lab.fta_abs not in \
                (Laboratorio.NO_APLICA, Laboratorio.NO_SE_HIZO):
                exams.append('FTA Abs: {}'.format(lab.fta_abs))
            if lab.tpha not in (Laboratorio.NO_APLICA, Laboratorio.NO_SE_HIZO):
                exams.append('THPA: {}'.format(lab.tpha))
            if lab.elisa not in \
                (Laboratorio.NO_APLICA, Laboratorio.NO_SE_HIZO):
                exams.append('ELISA: {}'.format(lab.elisa))
            if lab.ifi_western_blot not in \
                (Laboratorio.NO_APLICA, Laboratorio.NO_SE_HIZO):
                exams.append(
                    'IFI Western Blot: {}'.format(lab.ifi_western_blot))
            if lab.htlv_1 not in \
                (Laboratorio.NO_APLICA, Laboratorio.NO_SE_HIZO):
                exams.append('HTLV 1: {}'.format(lab.htlv_1))
            if lab.torch not in \
                (Laboratorio.NO_APLICA, Laboratorio.NO_SE_HIZO):
                exams.append('TORCH: {}'.format(lab.torch))
            if lab.gota_gruesa not in \
                (Laboratorio.NO_APLICA, Laboratorio.NO_SE_HIZO):
                exams.append('Gota gruesa: {}'.format(lab.gota_gruesa))
            if lab.malaria_prueba_rapida not in \
                (Laboratorio.NO_APLICA, Laboratorio.NO_SE_HIZO):
                exams.append(
                    'Malaria prueba rapida: {}'.format(
                        lab.malaria_prueba_rapida))
            if lab.fluorencia_malaria not in \
                (Laboratorio.NO_APLICA, Laboratorio.NO_SE_HIZO):
                exams.append(
                    'Fluorescencia malaria: {}'.format(lab.fluorencia_malaria))
            if lab.examen_completo_orina_1 != Laboratorio.NO_SE_HIZO:
                exams.append(
                    'Examen completo orina 1: {}'.format(
                        lab.examen_completo_orina_1))
            if lab.examen_completo_orina_2 != Laboratorio.NO_SE_HIZO:
                exams.append(
                    'Examen completo orina 2: {}'.format(
                        lab.examen_completo_orina_2))
            if lab.leucocituria != Laboratorio.NO_SE_HIZO:
                exams.append('Leucocituria: {}'.format(lab.leucocituria))
            if lab.nitritos != Laboratorio.NO_SE_HIZO:
                exams.append('Nitritos: {}'.format(lab.nitritos))
            if lab.urocultivo not in \
                (Laboratorio.NO_APLICA, Laboratorio.NO_SE_HIZO):
                exams.append('Urocultivo: {}'.format(lab.urocultivo))
            if lab.bk_en_esputo not in \
                (Laboratorio.NO_APLICA, Laboratorio.NO_SE_HIZO):
                exams.append('BK en esputo: {}'.format(lab.bk_en_esputo))
            if lab.listeria not in \
                (Laboratorio.NO_APLICA, Laboratorio.NO_SE_HIZO):
                exams.append('Listeria: {}'.format(lab.listeria))
            if lab.tamizaje_hepatitis_b not in \
                (Laboratorio.NO_APLICA, Laboratorio.NO_SE_HIZO):
                exams.append(
                    'Tamizaje Hepatitis B: {}'.format(
                        lab.tamizaje_hepatitis_b))
            if lab.pap not in (Laboratorio.NO_APLICA, Laboratorio.NO_SE_HIZO):
                exams.append('PAP: {}'.format(lab.pap))
            if lab.iva not in (Laboratorio.NO_APLICA, Laboratorio.NO_SE_HIZO):
                exams.append('IVA: {}'.format(lab.iva))
            if lab.colposcopia not in \
                (Laboratorio.NO_APLICA, Laboratorio.NO_SE_HIZO):
                exams.append('Colposcopia: {}'.format(lab.colposcopia))
            return ', '.join(exams)
        return ''


class CarneControlPrenatalReport(BaseJasperReport):
    report_name = 'carne_control_prenatal'

    def __init__(self, control):
        self.control = control
        self.filename = 'carne_control_prenatal_{}_{}'.format(
            control.paciente.tipo_documento.upper(),
            control.paciente.numero_documento
        )
        super(CarneControlPrenatalReport, self).__init__()

    def get_params(self):
        ganancia_peso = self.control.embarazo.chart_ganancia_peso_materno

        if ganancia_peso.name:
            ganancia_peso_path = ''.join(['', '{0}/media/{1}'.format(settings.DOMAIN, ganancia_peso.name)])
        else:
            ganancia_peso_path = ''

        altura_uterina = self.control.embarazo.chart_altura_uterina

        if altura_uterina.name:
            altura_uterina_path = ''.join(['', '{0}/media/{1}'.format(settings.DOMAIN, altura_uterina.name)])
        else:
            altura_uterina_path = ''

        logo_minsa = '{0}/static/img/logo_minsa.png'.format(settings.DOMAIN)

        result = {
            'control_id': str(self.control.id),
            'paciente_id': str(self.control.paciente.id),
            'embarazo_id': str(self.control.embarazo.id),
            'ganancia_peso_chart': ganancia_peso_path,
            'altura_uterina_chart': altura_uterina_path,
            'minsa_logo': logo_minsa
        }

        return result


class SolicitudExamenCitologicoReport(BaseJasperReport):
    report_name = 'solicitud_examen_citologico'

    def __init__(self, control):
        self._control = control
        self._paciente = control.paciente
        self.filename = 'solicitud_examen_citologico_{}_{}'.format(
            self._paciente.tipo_documento.upper(),
            self._paciente.numero_documento)
        super(SolicitudExamenCitologicoReport, self).__init__()

    def get_params(self):
        diresa_logo = self._control.establecimiento.diresa.logo

        if diresa_logo.name:
            diresa_logo_path = '/'.join([
                settings.MEDIA_ROOT, diresa_logo.name])
        else:
            diresa_logo_path = ''

        establecimiento_logo = self._control.establecimiento.logo

        if establecimiento_logo.name:
            establecimiento_logo_path = '/'.join([
                settings.MEDIA_ROOT, establecimiento_logo.name])
        else:
            establecimiento_logo_path = ''

        return {
            'control_id': str(self._control.id),
            'diresa_logo': diresa_logo_path or 'not',
            'establecimiento_logo': establecimiento_logo_path or 'not'
        }


class SolicitudPruebaElisaReport(BaseJasperReport):
    report_name = 'solicitud_prueba_elisa'

    def __init__(self, control, establecimiento_id):
        self._control = control
        self._establecimiento_id = establecimiento_id
        self.filename = 'solicitud_prueba_elisa_{}_{}'.format(
            self._control.paciente.numero_documento,
            datetime.today().strftime('%d/%m/%Y'))
        super(SolicitudPruebaElisaReport, self).__init__()

    def get_params(self):
        logo_minsa = '{0}/static/img/logo_minsa.png'.format(settings.DOMAIN)

        return {
            'control_id': self._control.id,
            'establecimiento_id': self._establecimiento_id,
            'logo_minsa': logo_minsa
        }


class ControlPrenatalExcelReport(object):
    control = None
    report_name = "control_prenatal"
    def __init__(self, control):
        self.control = control


    def signed_report(self, identifier, path_next, buffer):
        try:
            doc = Document.objects.get(identifier=identifier, signed_file='')
        except Document.DoesNotExist:
            doc = Document.new('{}_{}.xlsx'.format(self.report_name, identifier), identifier, buffer, "other")
        return redirect('{}?next={}'.format(reverse('firma:sign-document', kwargs={'document_id': doc.id}), path_next))


    def render_signed_file(self, identifier):
        qr = Document.objects.filter(identifier=identifier).exclude(signed_file='')
        if qr.count() == 1:
            doc = qr[0]
            response = HttpResponse(content_type=doc.content_type)
            response['Content-Disposition'] = 'attachment; filename="{}.p7m"'.format(doc.name)
            response.write(doc.signed_file.read())
            return response
        else:
            raise Http404


    def get_book(self, output):
        wb = xlsxwriter.Workbook(output)

        common_format = {
            'valign': 'vcenter'
        }

        def _add_format(properties):
            tmp = common_format.copy()
            tmp.update(properties)
            _format = wb.add_format(tmp)
            _format.set_text_wrap()
            return _format

        paciente = self.control.paciente

        datoscompletos = "%s %s , %s" % (paciente.apellido_paterno, paciente.apellido_materno, paciente.nombres)
        numerodocumento = paciente.numero_documento
        numerohistoria = paciente.historias_clinicas.last().numero
        informacion_pie_pagina = '&L&"Arial,Bold"PACIENTE: &"Arial"%s  &"Arial,Bold"DNI: &"Arial"%s &"Arial,Bold"HC: &"Arial"%s' % (
            datoscompletos, numerodocumento, numerohistoria)

        title_format = _add_format({
            'bold': True,
            'size': 15,
            'underline': True
        })

        bordered = _add_format({
            'border': 1,
            'align': 'center'
        })

        measure_label_format = _add_format({
            'bold': True
        })

        sheet = wb.add_worksheet('Hoja 1')
        sheet.set_footer(informacion_pie_pagina)
        sheet.set_portrait()
        sheet.fit_to_pages(1, 0)
        cols_withs = (
            ('A', 10), ('B', 10), ('C', 8),
            ('D', 1), ('E', 8), ('F', 8),
            ('G', 8), ('H', 1), ('I', 12),
            ('J', 8), ('K', 12), ('L', 1),
            ('M', 8), ('N', 1), ('O', 8),
            ('P', 8)
        )
        for col_name, width in cols_withs:
            sheet.set_column('{0}:{0}'.format(col_name), width)
        row_heights = (
            (9, 40), (11, 40), (13, 40), (15, 40)
        )
        for row_number, height in row_heights:
            sheet.set_row(row_number, height)

        sheet.insert_image('A1', settings.STATIC_ROOT + '/img/logo_minsa.png', {'x_scale': 0.5, 'y_scale': 0.5})

        sheet.merge_range(
            'D1:P1', u'CONTROL PRENATAL Nº {}'.format(self.control.numero),
            title_format)
        sheet.write_string('D3', 'Fecha:')
        sheet.write_string(
            'F3', self.control.atencion_fecha.strftime('%d/%m/%Y'))
        sheet.write_string('H3', 'Hora:')
        sheet.write_string(
            'J3', self.control.atencion_hora.strftime('%H:%M'), bordered)
        sheet.merge_range('A5:P5', 'SUBJETIVO:', title_format)
        sheet.merge_range(
            'A6:P6', u'Gestante acude al control prenatal º {}'.format(
                self.control.numero))
        if not self.control.asintomatica:
            sintomas = ', '.join([
                sintoma.cie.nombre_mostrar for sintoma in
                self.control.sintomas.all()])
            sheet.merge_range(
                'A7:P7', u'Refiere los siguiente síntomas: {}'.format(
                    sintomas))
        else:
            sintomas = u'Asintomática'
            sheet.merge_range('A7:P7', u'No refiere síntomas')
        sheet.merge_range('A9:P9', 'OBJETIVO:', title_format)
        '''
        labels = (
            ('A10', u'Presión arterial'),
            ('A12', 'Peso actual'),
            ('A14', 'Altura uterina'),
            ('A16', 'Mov. fetales'),
            ('E10', 'Pulso'),
            ('E12', 'IMC'),
            ('E14', 'FCF'),
            ('E16', u'Dinámica uterina'),
            ('I10', 'Frecuencia respiratoria'),
            ('I14', u'Situación'),
            ('I16', 'Edemas'),
            ('K14', u'Presentación'),
            ('K16', 'Reflejos'),
            ('M10', 'Temp.'),
            ('O14', u'Posición'),
            ('O16', u'Examen pezón')
        )

        units = (
            ('C10', 'mmHg'),
            ('C12', 'kg'),
            ('C14', 'cm'),
            ('F10', 'x minuto'),
            ('G14', 'lat/min'),
            ('K10', 'x minuto'),
            ('P10', u'ºC'),
        )
        '''
        examenes_fisico_fetales = ExamenFisicoFetal.objects.filter(control=self.control)

        labels = (
            ('A10', u'Presión arterial'),
            ('A12', 'Peso actual'),
            ('A14', 'Altura uterina'),
            ('A16', 'Mov. fetales'),
            ('E10', 'Pulso'),
            ('E12', 'IMC'),
            ('E14', u'Dinámica uterina'),
            ('E16', 'FCF'),
            ('I10', 'Frecuencia respiratoria'),
            ('I14', 'Edemas'),
            ('I16', u'Situación'),
            ('K14', 'Reflejos'),
            ('K16', u'Presentación'),
            ('M10', 'Temp.'),
            ('O14', u'Examen pezón'),
            ('O16', u'Posición')
        )

        units = (
            ('C10', 'mmHg'),
            ('C12', 'kg'),
            ('C14', 'cm'),
            ('F10', 'x minuto'),
            ('G16', 'lat/min'),
            ('K10', 'x minuto'),
            ('P10', u'ºC'),
        )

        for cell, label in labels:
            sheet.write_string(cell, label, measure_label_format)

        indice = 16

        if len(examenes_fisico_fetales) > 1:

            for i in range(1, len(examenes_fisico_fetales)):
                indice += 2

                labels_exf = (
                    ('A{}'.format(indice), 'Mov. fetales'),
                    ('E{}'.format(indice), 'FCF'),
                    ('I{}'.format(indice), u'Situación'),
                    ('K{}'.format(indice), u'Presentación'),
                    ('O{}'.format(indice), u'Posición')
                )

                for cell, label in labels_exf:
                    sheet.write_string(cell, label, measure_label_format)
                    sheet.set_row(indice - 1, 40)

                    if cell == 'E{}'.format(indice):
                        sheet.write_string('G{}'.format(indice), 'lat/min')

        for cell, name in units:
            sheet.write_string(cell, name)

        measures = (
            ('B10', 'presion_arterial'),
            ('B12', 'peso'),
            ('B14', 'altura_uterina'),
            ('B16', 'movimientos_fetales'),
            ('F10', 'pulso'),
            ('F12', 'imc'),
            ('F14', 'dinamica_uterina'),
            ('F16', 'fcf'),
            ('J10', 'frecuencia_respiratoria'),
            ('J14', 'edemas'),
            ('J16', 'situacion'),
            ('M14', 'reflejos'),
            ('M16', 'presentacion'),
            ('O10', 'temperatura'),
            ('P14', 'examen_pezon'),
            ('P16', 'posicion')
        )
        for cell, field_name in measures:
            field = getattr(self.control, field_name)
            sheet.write_string(
                cell, str(field).upper() if field else '', bordered)

        indice_exf = 14
        if len(examenes_fisico_fetales) > 0:
            for i in range(0, len(examenes_fisico_fetales)):
                indice_exf += 2

                measures_exf = (
                    ('B{}'.format(indice_exf), 'movimientos_fetales'),
                    ('F{}'.format(indice_exf), 'fcf'),
                    ('J{}'.format(indice_exf), 'situacion'),
                    ('M{}'.format(indice_exf), 'presentacion'),
                    ('P{}'.format(indice_exf), 'posicion')
                )
                examen_fisico_fetal = examenes_fisico_fetales[i]

                for cell, field_name in measures_exf:
                    field = getattr(examen_fisico_fetal, field_name)
                    sheet.write_string(cell, str(field).upper() if field else '', bordered)

        def _d2str(_field):
            return '({})'.format(_field.strftime('%d-%m-%Y')) if _field else ''

        if hasattr(self.control, 'laboratorio') and self.control.laboratorio:
            indice += 2
            examenes_lab = self.control.laboratorio.examenes_con_resultado
            if examenes_lab:
                lab_format = _add_format({})
                # sheet.merge_range('A18:P18', u'Exámenes de laboratorio')
                sheet.merge_range('A{}:P{}'.format(indice, indice), u'Exámenes de laboratorio')

                exams_formatted = map(
                    lambda x: u'{}: {} {}'.format(
                        x[0], x[1], _d2str(x[2])), examenes_lab)

                indice += 1
                # sheet.merge_range('A19:P20', u', '.join(exams_formatted), lab_format)
                sheet.merge_range('A{}:P{}'.format(indice, indice + 1), u', '.join(exams_formatted), lab_format)

        indice += 4
        # sheet.merge_range('A22:P22', u'APRECIACIÓN', title_format)
        sheet.merge_range('A{}:P{}'.format(indice, indice), u'DIAGNÓSTICO', title_format)
        indice += 1

        # 'A23:P23', u'Paciente mujer de '
        cell_ = 'A{0}:P{1}'.format(indice, indice)
        sheet.merge_range(
            cell_, u'Paciente mujer de '
                   u'{} años, con {} semanas de gestación por {}'.format(
                self.control.paciente.edad,
                self.control.edad_gestacional_semanas,
                self.control.eg_elegida.upper()))

        def _current_row_merge(col):
            return 'A{0}:P{0}'.format(col)

            # row_counter = 24

        row_counter = indice + 1
        if hasattr(self.control, 'diagnostico') and self.control.diagnostico:
            dxs = [dx.cie for dx in self.control.diagnostico.detalles.all()]
            if dxs:
                # sheet.merge_range('A24:P24', u'Con los siguientes diagnósticos:')
                sheet.merge_range('A{}:P{}'.format(row_counter, row_counter), u'Con los siguientes diagnósticos:')
                row_counter += 1
            dxs.sort()
            for dx in dxs:
                tmp_dx = ' - '.join([
                    dx.codigo.upper(), dx.nombre_display.upper()])

                sheet.merge_range(_current_row_merge(row_counter), tmp_dx)
                row_counter += 1

        sheet.merge_range(
            _current_row_merge(row_counter), 'PLAN', title_format)
        row_counter += 1
        ocs = self.control.consejerias_realizadas

        if ocs:
            sheet.merge_range(
                _current_row_merge(row_counter),
                u'Se le brindaron las siguientes consejerías: {}'.format(
                    u', '.join(ocs)))
            row_counter += 1
        if hasattr(self.control, 'diagnostico') and self.control.diagnostico:
            tratamientos = []
            if self.control.indicacion_hierro:
                tratamientos.append(
                    u'Sulfato ferroso: {} tabletas'.format(
                        self.control.indicacion_hierro))
            if self.control.indicacion_calcio:
                tratamientos.append(
                    u'Calcio: {} tabletas'.format(
                        self.control.indicacion_calcio))
            if self.control.indicacion_acido_folico:
                tratamientos.append(
                    u'Ácido fólico: {} tabletas'.format(
                        self.control.indicacion_acido_folico))
            if self.control.indicacion_hierro_acido_folico:
                tratamientos.append(
                    u'Sulfato ferroso / ácido fólico: {} tabletas'.format(
                        self.control.indicacion_hierro_acido_folico))
            if tratamientos:
                sheet.merge_range(
                    _current_row_merge(row_counter), 'TRATAMIENTO', title_format)
                row_counter += 1
                sheet.merge_range(
                    _current_row_merge(row_counter),
                    u'Tratamiento: {}'.format('\n'.join(tratamientos)))
                row_counter += 1
            examenes_a_pedir = self.control.diagnostico.examenes_a_pedir
            if examenes_a_pedir:
                sheet.merge_range(
                    _current_row_merge(row_counter),
                    u'Se le pidió los siguientes exámenes: {}'.format(
                        examenes_a_pedir))
                row_counter += 1
            if self.control.diagnostico.plan_trabajo:
                sheet.merge_range(
                    _current_row_merge(row_counter),
                    self.control.diagnostico.plan_trabajo)
        row_counter += 8
        sheet.merge_range(
            _current_row_merge(row_counter),
            self.control.created_by.get_full_name())
        row_counter += 1
        sheet.merge_range(
            _current_row_merge(row_counter),
            u'Nº Colegio: {}'.format(
                self.control.created_by.colegiatura or ''))
        wb.close()
        return wb
