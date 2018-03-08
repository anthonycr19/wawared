# coding:utf-8
from __future__ import unicode_literals
import calendar
from datetime import timedelta, datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, IntegrityError, connection
from django.conf import settings
from django.db.models import Count, Q
from easy_thumbnails.files import get_thumbnailer
import xlsxwriter

from controles import Control
from controles.models import Laboratorio, ExamenFisicoFetal
from embarazos.models import Embarazo, Ecografia
from pacientes.models import HistoriaClinica
from partos.models import Partograma, Ingreso, TerminacionEmbarazo
from puerperio.models import Monitoreo, TerminacionPuerpera


def get_hc(paciente, establecimiento):
    try:
        hc = HistoriaClinica.objects.get(
            paciente=paciente, establecimiento=establecimiento)
        return hc.numero
    except HistoriaClinica.DoesNotExist:
        return ''


class SIENReport(object):
    establecimiento = None

    def __init__(self, establecimiento, filter_date, period):
        self.establecimiento = establecimiento
        self.filter_date = filter_date
        self.period = period
        super(SIENReport, self).__init__()

    def _get_week_limits(self):
        _date = self.filter_date
        while calendar.weekday(_date.year, _date.month, _date.day):
            _date += timedelta(days=-1)
        return _date, _date + timedelta(days=+6)

    def _get_query_set(self):
        _filters = {
            'hemoglobina_1': True
        }

        params = ""
        params2 = ""

        if self.period == 'daily':
            _filters['control__atencion_fecha'] = self.filter_date
            params = " = '{0}'".format(self.filter_date)
            params2 = " = '{0}'".format(self.filter_date)
        else:
            _filters['control__atencion_fecha__range'] = self._get_week_limits()
            params = " between '{0}' and '{1}'".format(self._get_week_limits()[0], self._get_week_limits()[1])
            params2 = " between '{0}' and '{1}'".format(self._get_week_limits()[0], self._get_week_limits()[1])

        # labs = Laboratorio.objects.prefetch_related('control').filter(**_filters)


        # control_ids = [lab.control.id for lab in labs]
        cursor = connection.cursor()

        sql = """select distinct a.id from
            (SELECT c.id
                FROM public.controles_laboratorio as cl inner join public.controles_control as c on c.id=cl.control_id
                WHERE hemoglobina_1=true and c.atencion_fecha {0}

                union all

                SELECT c.id
                FROM public.controles_laboratorio as cl inner join public.embarazos_embarazo as e on e.id=cl.embarazo_id
                inner join public.controles_control as c on c.embarazo_id = e.id
                WHERE hemoglobina_1=true and c.atencion_fecha {1}
                ) as a
                """
        sql = sql.format(params, params2)

        cursor.execute(sql)

        control_ids = (row[0] for row in cursor.fetchall())

        paciente_ids = []
        ids = []
        qs = Control.objects.filter(
            id__in=control_ids, establecimiento=self.establecimiento).order_by(
            'atencion_fecha').values('paciente_id', 'id')
        for control in qs:
            if control['paciente_id'] not in paciente_ids:
                ids.append(control['id'])
                paciente_ids.append(control['paciente_id'])
        return Control.objects.prefetch_related(
            'paciente', 'establecimiento').filter(id__in=ids)

    def get_book(self, output):
        wb = xlsxwriter.Workbook(output, {
            'default_date_format': 'dd/mm/yyyy'
        })
        sheet = wb.add_worksheet('Hoja 1')
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)

        sheet.merge_range(
            'A2:R2', 'SISTEMA DE INFORMACION DEL ESTADO NUTRICIONAL',
            wb.add_format({
                'align': 'center',
                'size': '16',
                'bold': True}))
        sheet.merge_range(
            'A3:R3', 'FORMATO DE REGISTRO DIARIO DE LA GESTANTE',
            wb.add_format({
                'align': 'center',
                'size': '12',
                'bold': True}))
        left_box_format_1 = wb.add_format({
            'align': 'left',
            'size': '11',
            'border': 1
        })
        left_box_format_2 = wb.add_format({
            'align': 'center',
            'size': '11',
            'border': 1
        })

        sheet.insert_image('A1', settings.STATIC_ROOT + '/img/minsa_logo.png')
        sheet.insert_image('E1', settings.STATIC_ROOT + '/img/ins_logo.jpg')
        if self.establecimiento.logo:
            options = {'size': (50, 50), 'crop': True}
            thumb = get_thumbnailer(
                self.establecimiento.logo).get_thumbnail(options)
            sheet.insert_image('R1', settings.MEDIA_ROOT + '/' + thumb.name)

        sheet.merge_range('A5:B5', 'DIRESA:', left_box_format_1)

        if self.establecimiento.diresa:
            sheet.merge_range(
                'C5:D5', self.establecimiento.diresa.nombre, left_box_format_2)
        else:
            sheet.merge_range('C5:D5', '', left_box_format_2)

        sheet.merge_range('A6:B6', 'RED:', left_box_format_1)
        sheet.merge_range(
            'C6:D6', self.establecimiento.red.nombre, left_box_format_2)
        sheet.merge_range('A7:B7', 'MICRORED:', left_box_format_1)

        if self.establecimiento.microred:
            sheet.merge_range(
                'C7:D7', self.establecimiento.microred.nombre,
                left_box_format_2)
        else:
            sheet.merge_range('C7:D7', '', left_box_format_2)

        sheet.merge_range('A8:B8', 'ESTABLECIMIENTO:', left_box_format_1)
        sheet.merge_range(
            'C8:D8', self.establecimiento.nombre, left_box_format_2)
        sheet.merge_range(
            'M7:Q7', 'V° B° de Jefatura de EESS:', wb.add_format({
                'align': 'center',
                'size': 11}))
        sheet.merge_range(
            'M8:Q8', 'Nota: Sólo se registrará la primera visita de cada '
                     'gestante en el mes', wb.add_format({
                'bold': 1,
                'align': 'center',
                'size': 11}))

        def cell_format(size, date=False):
            _tmp = {
                'align': 'center',
                'size': size,
                'valign': 'vcenter',
                'border': 1
            }
            if date:
                _tmp['num_format'] = 'dd/mm/yyyy'
            _format = wb.add_format(_tmp)
            _format.set_text_wrap()
            return _format

        sheet.set_row(9, 20)
        sheet.set_row(10, 20)
        sheet.merge_range(
            'A10:A11', 'FECHA DE ATENCIÓN  (dd/mm/aa)', cell_format(10))
        sheet.merge_range(
            'B10:B11', 'SEMANA EPIDEMIOLÓGICA (SE)', cell_format(8))
        sheet.merge_range('C10:C11', 'N°', cell_format(11))
        sheet.merge_range('D10:D11', 'D.N.I.', cell_format(11))
        sheet.merge_range(
            'E10:E11', 'N° HISTORIA CLÍNICA (H.C.)', cell_format(11))
        sheet.merge_range('F10:F11', 'EDAD (años)', cell_format(9))
        sheet.merge_range(
            'G10:G11', 'EDAD GESTACIONAL (semanas)', cell_format(8))
        sheet.merge_range('H10:H11', 'PESO Actual (Kg)', cell_format(11))
        sheet.merge_range('I10:I11', 'TALLA (cm)', cell_format(11))
        sheet.merge_range('J10:J11', 'PESO PRE-GESTAC. (Kg)', cell_format(10))
        sheet.merge_range('K10:L10', 'TIPO DE EMBARAZO', cell_format(8))
        sheet.write('K11', 'Unico(U)', cell_format(8))
        sheet.write('L11', 'MULTIPLE(M)', cell_format(8))
        sheet.merge_range('M10:M11', 'HEMO-GLOBINA (gr/dL)', cell_format(9))
        sheet.merge_range(
            'N10:N11', 'FECHA DE EXAMEN DE HEMOGLOBINA', cell_format(8))
        sheet.merge_range('O10:Q10', 'LUGAR DE RESIDENCIA', cell_format(11))
        sheet.write('O11', 'PROVINCIA', cell_format(9))
        sheet.write('P11', 'DISTRITO', cell_format(9))
        sheet.write('Q11', 'LOCALIDAD', cell_format(11))
        sheet.merge_range(
            'R10:R11', 'ALTITUD DE LA LOCALIDAD (msnm)', cell_format(8))

        common_cell_format = cell_format(11)
        date_format = cell_format(11, date=True)

        _row = 11
        for column_name in 'ABCDEFGHIJKLMNOPQR':
            sheet.set_column('{c}:{c}'.format(c=column_name), 11)
        qs = self._get_query_set()
        for control in qs:
            last_ecografia = control.embarazo.ecografias.last()
            sheet.set_row(_row, 20)
            sheet.write_datetime(_row, 0, control.atencion_fecha, date_format)
            sheet.write(_row, 1, '', common_cell_format)
            sheet.write(_row, 2, control.numero, common_cell_format)
            sheet.write(
                _row, 3, control.paciente.numero_documento, common_cell_format)
            sheet.write(
                _row, 4, get_hc(control.paciente, control.establecimiento),
                common_cell_format)
            sheet.write(_row, 5, control.paciente.edad, common_cell_format)
            sheet.write(
                _row, 6, control.edad_gestacional_semanas, common_cell_format)
            sheet.write(_row, 7, control.peso, common_cell_format)
            sheet.write(_row, 8, control.embarazo.talla, common_cell_format)
            sheet.write(_row, 9, control.embarazo.peso, common_cell_format)
            unico_content = ''
            multiple_content = ''
            if last_ecografia is not None:
                if last_ecografia.tipo_embarazo == Ecografia.TIPO_UNICO:
                    unico_content = 'X'
                else:
                    unico_content = ''

                if last_ecografia.tipo_embarazo == Ecografia.TIPO_MULTIPLE:
                    multiple_content = 'X'
                else:
                    multiple_content = ''

            sheet.write(_row, 10, unico_content, common_cell_format)
            sheet.write(_row, 11, multiple_content, common_cell_format)

            try:
                if hasattr(control, 'laboratorio'):
                    labo = control.laboratorio
                else:
                    labo = Laboratorio.objects.get(embarazo=control.embarazo)
            except ObjectDoesNotExist as e:
                labo = None
            '''
            if hasattr(control, 'laboratorio') and control.laboratorio:
                sheet.write(
                    _row, 12, control.laboratorio.hemoglobina_1_resultado,
                    common_cell_format)
            else:
                sheet.write(_row, 12, '', common_cell_format)

            if hasattr(control, 'laboratorio') and control.laboratorio and \
                    control.laboratorio.hemoglobina_1_fecha:
                sheet.write_datetime(
                    _row, 13, control.laboratorio.hemoglobina_1_fecha,
                    date_format)
            else:
                sheet.write(_row, 13, '', common_cell_format)
            '''
            if not labo is None:
                sheet.write(_row, 12, labo.hemoglobina_1_resultado, common_cell_format)
                if labo.hemoglobina_1_fecha:
                    sheet.write_datetime(_row, 13, labo.hemoglobina_1_fecha, date_format)
                else:
                    sheet.write(_row, 13, '', common_cell_format)

            else:
                sheet.write(_row, 12, '', common_cell_format)
                sheet.write(_row, 13, '', common_cell_format)

            sheet.write(
                _row, 14, control.paciente.provincia_residencia.nombre,
                common_cell_format)
            sheet.write(
                _row, 15, control.paciente.distrito_residencia.nombre,
                common_cell_format)
            sheet.write(
                _row, 16, control.paciente.urbanizacion, common_cell_format)
            sheet.write(_row, 17, '', common_cell_format)
            _row += 1
        if qs.count() < 20:
            for i in range(20 - qs.count()):
                sheet.set_row(_row, 20)
                for j in range(18):
                    sheet.write(_row, j, '', common_cell_format)
                _row += 1
        _row += 1
        sheet.merge_range(_row, 2, _row, 17, 'OBSERVACIONES:')
        _row += 2
        sheet.write(_row, 0, 'RESPONSABLE DEL REGISTRO:')
        sheet.write(_row, 5, 'RESPONSABLE DEL CONTROL DE CALIDAD DE FRD:')
        sheet.write(_row, 13, 'RESPONSABLE DE ENTREGA DE FRD:')
        sheet.write(_row + 2, 0, 'FIRMA:')
        sheet.write(_row + 2, 5, 'FIRMA:')
        sheet.write(_row + 2, 13, 'RECEPCIONADO POR:')
        sheet.write(
            _row + 4, 0,
            u'*Asignar los nombres de las localidades según la forma como '
            u'está sectorizado el EE. SS. No considerar Avenidas, Jirones, '
            'Calles, etc.')
        return wb


class GlobalReport(object):
    establecimiento_ids = None

    def __init__(self, establecimiento_ids, start_date, end_date):
        self.establecimiento_ids = establecimiento_ids
        self.start_date = start_date
        self.end_date = end_date
        super(GlobalReport, self).__init__()

    def get_queryset(self):
        return Embarazo.objects.prefetch_related(
            'controles', 'paciente', 'establecimiento').annotate(
            controles_quantity=Count('controles')).filter(
            controles_quantity__gte=1,
            establecimiento_id__in=self.establecimiento_ids)

    def get_book(self, output):
        wb = xlsxwriter.Workbook(output, {
            'default_date_format': 'dd/mm/yyyy'
        })
        sheet = wb.add_worksheet('Hoja 1')
        header_format = wb.add_format()
        header_format.set_bg_color('yellow')
        header_format.set_border()
        date_col_size = 10
        for _index in range(2000):
            sheet.set_column(_index, _index, date_col_size)
        headers = (
            ('A1', 'Control_1_fecha'),
            ('B1', 'Establecimiento'),
            ('C1', 'HC'),
            ('D1', 'DNI'),
            ('E1', 'Apellido paterno'),
            ('F1', 'Apellido materno'),
            ('G1', 'Nombres'),
            ('H1', 'Edad'),
            ('I1', 'Fecha de nacimiento'),
            ('J1', 'Transfusion_sanguinea'),
            ('K1', 'DNI_Responsable'),
            ('L1', 'Nombre_resposable'),
            ('M1', 'Tipo_parentezco_responsable'),
            ('N1', 'Lugar_nacimiento_pais'),
            ('O1', 'Lugar_nacimiento_departamento'),
            ('P1', 'Lugar_nacimiento_provincia'),
            ('Q1', 'Departamento_residencia'),
            ('R1', 'Provincia_residencia'),
            ('S1', 'Distrito_residencia'),
            ('T1', 'Sector_residencia'),
            ('U1', 'Direccion_residencia'),
            ('V1', 'Telefono_casa'),
            ('W1', 'Celular'),
            ('X1', 'Operaror_celular'),
            ('Y1', 'Correo_electronico'),
            ('Z1', 'Educacion'),
            ('AA1', 'Años_aprobados'),
            ('AB1', 'Ocupacion'),
            ('AC1', 'Estado_civil'),
            ('AD1', 'Etnia'),
            ('AE1', 'Tipo_seguro'),
            ('AF1', 'Componente'),
            ('AG1', 'Afiliacion'),
            ('AH1', 'Codigo_afiliacion'),
            ('AI1', 'Antecedentes_familiares'),
            ('AJ1', 'Antecedentes_medicos'),
            ('AK1', 'Fecha_ultima_gestacion'),
            ('AL1', 'Embarazos_previos_gestas'),
            ('AM1', 'Embarazos_previos_abortos'),
            ('AN1', 'Embarazos_previos_partos'),
            ('AO1', 'Embarazos_previos_vaginales'),
            ('AP1', 'Embarazos_previos_edad_cesareas'),
            ('AQ1', 'Embarazos_previos_nacidos_vivos'),
            ('AR1', 'Embarazos_previos_nacidos_muertos'),
            ('AS1', 'Embarazos_previos_viven'),
            ('AT1', 'embarazos_previos_muertos_1ra_sem'),
            ('AU1', 'embarazos_previos_despues_1ra_sem'),
            ('AV1', 'embarazos_previos_0_3'),
            ('AW1', 'embarazos_previos_menor_2500g'),
            ('AX1', 'embarazos_previos_multiple'),
            ('AY1', 'embarazos_previos_menor_37sem'),
            ('AZ1', 'embarazos_previos_viven'),
            ('BA1', 'Menarquia_edad'),
            ('BB1', 'andria'),
            ('BC1', 'edad_1ra_relacion_sexual'),
            ('BD1', 'regimen_catameneal'),
            ('BE1', 'duracion_menstruacion'),
            ('BF1', 'ciclo_menstruacion'),
            ('BG1', 'Papanicolao'),
            ('BH1', 'fecha_papanicolao'),
            ('BI1', 'resultado_papanicolao'),
            ('BJ1', 'lugar_papanicolao'),
            ('BK1', 'ultimo_metodo_anticonceptivo'),
            ('BL1', 'embarazo_usando_MAC'),
            ('BM1', 'vacuna_rubeola'),
            ('BN1', 'vacuna_hepatitis'),
            ('BO1', 'vacuna_papiloma'),
            ('BP1', 'vacuna_fiebre_amarilla'),
            ('BQ1', 'vacuna_antitetanica_dosis'),
            ('BR1', 'antitetanica_1ra_dosis'),
            ('BS1', 'antitetanica_2da_dosis'),
            ('BT1', 'antitetanica_3ra_dosis'),
            ('BU1', 'nombre_padre'),
            ('BV1', 'FUM'),
            ('BW1', 'FUM_confiable'),
            ('BX1', 'captada'),
            ('BY1', 'referida'),
            ('BZ1', 'Talla'),
            ('CA1', 'Peso_habitual'),
            ('CB1', 'IMC'),
            ('CC1', 'EG_actual_FUM'),
            ('CD1', 'fecha_probable_FUM'),
            ('CE1', 'Violencia'),
            ('CF1', 'Quien'),
            ('CG1', 'hematomas'),
            ('CH1', 'cicatrices'),
            ('CI1', 'laceracion_boca'),
            ('CJ1', 'quejas_cronicas'),
            ('CK1', 'cefalea_problemas_sueno'),
            ('CL1', 'problemas_apetito'),
            ('CM1', 'extrema_falta_confianza'),
            ('CN1', 'tristeza_depresion'),
            ('CO1', 'retraimiento'),
            ('CP1', 'llanto_frecuente'),
            ('CQ1', 'uso_drogas'),
            ('CR1', 'numero_cigarros'),
            ('CS1', 'depresion_perdida_interes'),
            ('CT1', 'depresion_triste_deprimida'),
            ('CU1', 'PHQ2 PUNTAJE'),
            ('CV1', 'Fecha de tamizaje'),
            ('CW1', 'poco_interes_en_hacer_cosas'),
            ('CX1', 'demasiado_depremida'),
            ('CY1', 'problemas_dormir'),
            ('CZ1', 'cansada_poca_energia'),
            ('DA1', 'poco_apetito_exceso'),
            ('DB1', 'sentirse_mal_de_si_mismo'),
            ('DC1', 'dificultad_poner_atencion'),
            ('DD1', 'mueve_habla_lento'),
            ('DE1', 'pensar_en_morir'),
            ('DF1', 'cumplir_trabajo'),
            ('DG1', 'PHQ9 PUNTAJE'),
            ('DH1', 'hospitalizacion'),
            ('DI1', 'hospitalizacion_fecha'),
            ('DJ1', 'hospitalizacion_diagnostico'),
            ('DK1', 'emergencia'),
            ('DL1', 'emergencia_fecha'),
            ('DM1', 'emergencia_diagnostico'),
            ('DN1', '1ra_Eco_Fecha'),
            ('DO1', '1ra_Eco_edad'),
            ('DP1', '2da_Eco_Fecha'),
            ('DQ1', '2da_Eco_edad'),
            ('DR1', '3ra_Eco_Fecha'),
            ('DS1', '3ra_Eco_edad'),
            ('DT1', 'lab_1ra_rap_sifilis'),
            ('DU1', 'lab_2ra_rap_sifilis'),
            ('DV1', 'lab_1ra_rap_VIH'),
            ('DW1', 'lab_2da_rap_VIH'),
            ('DX1', 'lab_grupo'),
            ('DY1', 'lab_factor_rh'),
            ('DZ1', 'lab_hb_rap'),
            ('EA1', 'lab_hb_1ra'),
            ('EB1', 'lab_hb_2da'),
            ('EC1', 'lab_hb_al_alta'),
            ('ED1', 'lab_glicemia_1'),
            ('EE1', 'lab_glicemia_2'),
            ('EF1', 'lab_completo_orina_1'),
            ('EG1', 'lab_completo_orina_2'),
            ('EH1', 'lab_leucocituria'),
            ('EI1', 'lab_nitritos'),
            ('EJ1', 'lab_vdrl_rpr_1'),
            ('EK1', 'lab_vdrl_rpr_2'),
            ('EL1', 'lab_elisa'),
            ('EM1', 'lab_pap'),
            ('EN1', 'lab_iva'),
            ('EO1', 'lab_colposcopia'),
            ('EP1', 'lab_western_blot'),
            ('EQ1', 'lab_htlv_1'),
            ('ER1', 'lab_torch'),
            ('ES1', 'lab_gota_gruesa'),
            ('ET1', 'lab_malaria_rap'),
            ('EU1', 'lab_fluorescencia_malaria'),
            ('EV1', 'lab_urocultivo'),
            ('EW1', 'lab_bk_esputo'),
            ('EX1', 'lab_listeria'),
            ('EY1', 'lab_hepatitis_b'),
            ('EZ1', 'lab_tolerancia_glucosa'),
            ('FA1', 'lab_fta_abs'),
            ('FB1', 'lab_thpa'),)

        for _cell, value in headers:
            sheet.write(_cell, value, header_format)

        column = 'FB'

        def get_column():
            def _next(v):
                return 'A' if v == 'Z' else chr(ord(v) + 1)

            def _evaluate(v):
                if v:
                    if v[0] == 'Z':
                        return 'A' + _evaluate(v[1:])
                    else:
                        return _next(v[0]) + v[1:]
                else:
                    return 'A'

            return _evaluate(column[::-1])[::-1]

        control_headers = (
            'Control_{}_CS',
            'Control_{}_usuario',
            'Control_{}_Fecha',
            'Control_{}_Peso',
            'Control_{}_imc',
            'Control_{}_EG',
            'Control_{}_FPP',
            'Control_{}_temperatura',
            'Control_{}_PA',
            'Control_{}_pulso',
            'Control_{}_FR',
            'Control_{}_AU',
            'Control_{}_FCF',
            'Control_{}_situacion',
            'Control_{}_presentacion',
            'Control_{}_posicion',
            'Control_{}_mov-fetales',
            'Control_{}_dinamica_uterina',
            'Control_{}_proteinuria',
            'Control_{}_edemas',
            'Control_{}_reflejos',
            'Control_{}_pezon',
            'Control_{}_Fe',
            'Control_{}_Ca(Cod. 1451)',
            'Control_{}_Acid_fo(Cod. 200)',
            'Control_{}_Fe_Acid_fo(Cod. 3512)',
            'Control_{}_perfil_biofisico',
            'Control_{}_prox_cita',
            'Control_{}_nro_sis',
            'Control_{}_orientacion',
            'Control_{}_Signos_alarma',
            'Control_{}_piel',
            'Control_{}_mamas',
            'Control_{}_respiratorio',
            'Control_{}_cardio',
            'Control_{}_odonto',
            'Control_{}_abdomen',
            'Control_{}_urinario',
            'Control_{}_neuro',
            'Control_{}_conciencia',
            'Control_{}_espe_vagina',
            'Control_{}_espe_cervix',
            'Control_{}_espe_fondo',
            'Control_{}_espe_obs',
            'Control_{}_tacto_cambios',
            'Control_{}_tacto_vagina',
            'Control_{}_tacto_utero',
            'Control_{}_tacto_hallazgos',
            'Control_{}_tacto_incorp',
            'Control_{}_tacto_liquido',
            'Control_{}_tacto_membranas',
            'Control_{}_tacto_anexos',
            'Control_{}_bishop',
            'Control_{}_exam_dolor',
            'Control_{}_exam_posicion',
            'Control_{}_exam_restos',
            'Control_{}_exam_culdocentesis',
            'Control_{}_exam_fondo_saco',
            'Control_{}_exam_mal_olor',
            'Control_{}_exam_vulva',
            'Control_{}_exam_genitales',
            'Control_{}_exam_vagina',
            'Control_{}_dx',
            'Control_{}_plan_trabajo',
            'Control_{}_examenes_pedir',
            'Control_{}_psicoprofilaxis_1',
            'Control_{}_psicoprofilaxis_2',
            'Control_{}_psicoprofilaxis_3',
            'Control_{}_psicoprofilaxis_4',
            'Control_{}_psicoprofilaxis_5',
            'Control_{}_psicoprofilaxis_6',
            'Control_{}_inter_psicologia_1',
            'Control_{}_inter_psicologia_2',
            'Control_{}_inter_psicologia_3',
            'Control_{}_inter_medicina_1',
            'Control_{}_inter_medicina_2',
            'Control_{}_inter_medicina_3',
            'Control_{}_inter_nutricion_1',
            'Control_{}_inter_nutricion_2',
            'Control_{}_inter_nutricion_3',
            'Control_{}_inter_odontología_1',
            'Control_{}_inter_odontología_2',
            'Control_{}_inter_odontología_3',
            'Control_{}_inter_enfermeria_1',
            'Control_{}_inter_enfermeria_2',
            'Control_{}_inter_enfermeria_3',
            'Control_{}_inter_laboratorio_1',
            'Control_{}_inter_laboratorio_2',
            'Control_{}_inter_laboratorio_3',
            'Control_{}_inter_ecografia_1',
            'Control_{}_inter_ecografia_2',
            'Control_{}_inter_ecografia_3')

        for number in range(1, 10):
            for value in control_headers:
                column = get_column()
                sheet.write(
                    '{}{}'.format(column, 1), value.format(number),
                    header_format)

        row_counter = 2

        plan_parto_headers = (
            ('AOM1', 'Plan_parto_e1_fecha'),
            ('AON1', 'Plan_parto_e1_distancia_tiempo'),
            ('AOO1', 'Plan_parto_e1_se_quedara_en_domicilio_actual'),
            ('AOP1', 'Plan_parto_e1_lugar_atencion'),
            ('AOQ1', 'Plan_parto_e1_razon_de_eleccion_lugar_atencion'),
            ('AOR1', 'Plan_parto_e2_fecha'),
            ('AOS1', 'Plan_parto_e2_edad_gestacional'),
            ('AOT1', 'Plan_parto_e2_lugar_atencion'),
            ('AOU1', 'Plan_parto_e2_posicion_parto'),
            ('AOV1', 'Plan_parto_e2_transporte'),
            ('AOW1', 'Plan_parto_e2_tiempo_llegada_1'),
            ('AOX1', 'Plan_parto_e2_tiempo_llegada_2'),
            ('AOY1', 'Plan_parto_e2_persona_que_acompaña_en_el_parto'),
            ('AOZ1', 'Plan_parto_e2_person_cuidara_hijos_en_casa'),
            ('APA1', 'Plan_parto_e2_donador_1_nombre'),
            ('APB1', 'Plan_parto_e2_donador_1_tipo_sangre'),
            ('APC1', 'Plan_parto_e2_donador_1_domicilio'),
            ('APD1', 'Plan_parto_e2_donador_1_edad'),
            ('APE1', 'Plan_parto_e2_donador_1_parentesco'),
            ('APF1', 'Plan_parto_e2_donador_2_nombre'),
            ('APG1', 'Plan_parto_e2_donador_2_tipo_sangre'),
            ('APH1', 'Plan_parto_e2_donador_2_domicilio'),
            ('API1', 'Plan_parto_e2_donador_2_edad'),
            ('APJ1', 'Plan_parto_e2_donador_2_parentesco'),)

        for _cell, value in plan_parto_headers:
            sheet.write(_cell, value, header_format)

        def cell(_column):
            return '{}{}'.format(_column, row_counter)

        def si_no_na(_value):
            if _value is None:
                return 'NA'
            elif _value:
                return 'SI'
            else:
                return 'NO'

        def upper_value(_value):
            if _value:
                return _value.upper()
            else:
                return ''

        for embarazo in self.get_queryset():
            paciente = embarazo.paciente
            ag = paciente.antecedente_ginecologico
            ao = paciente.antecedente_obstetrico
            controles = embarazo.controles.filter(
                atencion_fecha__range=[self.start_date, self.end_date])
            if embarazo is None or not controles.count():
                continue
            first_control = controles.first()
            sheet.write_datetime(cell('A'), first_control.atencion_fecha or '')
            sheet.write(cell('B'), first_control.establecimiento.nombre or '')
            sheet.write(
                cell('C'), get_hc(paciente, first_control.establecimiento or '')),
            sheet.write(cell('D'), paciente.numero_documento or '')
            sheet.write(cell('E'), paciente.apellido_paterno or '')
            sheet.write(cell('F'), paciente.apellido_materno or '')
            sheet.write(cell('G'), paciente.nombres or '')
            sheet.write(cell('H'), paciente.edad or '')
            sheet.write_datetime(cell('I'), paciente.fecha_nacimiento or '')
            sheet.write(
                cell('J'), 'SI' if paciente.transfusion_sanguinea else 'NO')
            sheet.write(cell('K'), paciente.dni_responsable or '')
            sheet.write(cell('L'), paciente.nombre_responsable or '')

            if paciente.tipo_parentesco_responsable is not None:
                sheet.write(
                    cell('M'), paciente.tipo_parentesco_responsable.upper())
            else:
                sheet.write(cell('M'), '')

            sheet.write(cell('N'), paciente.pais_nacimiento.nombre)

            if paciente.departamento_nacimiento is not None:
                sheet.write(cell('O'), paciente.departamento_nacimiento.nombre)
            else:
                sheet.write(cell('O'), '')

            if paciente.provincia_nacimiento is not None:
                sheet.write(cell('P'), paciente.provincia_nacimiento.nombre)
            else:
                sheet.write(cell('P'), '')

            sheet.write(cell('Q'), paciente.departamento_residencia.nombre if paciente.departamento_residencia else '')
            sheet.write(cell('R'), paciente.provincia_residencia.nombre if paciente.provincia_residencia else '')
            sheet.write(cell('S'), paciente.distrito_residencia.nombre if paciente.distrito_residencia else '')
            sheet.write(cell('T'), paciente.urbanizacion or '')
            sheet.write(cell('U'), paciente.direccion or '')
            sheet.write(cell('V'), paciente.telefono or '')
            sheet.write(cell('W'), paciente.celular or '')
            sheet.write(cell('X'), paciente.operador.capitalize() or '')
            sheet.write(cell('Y'), paciente.email or '')
            sheet.write(cell('Z'), paciente.estudio_nombre.capitalize() if paciente.estudio_nombre else '')
            sheet.write(cell('AA'), paciente.tiempo_estudio or '')
            sheet.write(cell('AB'), paciente.ocupacion_nombre or '')

            if paciente.estado_civil is not None:
                sheet.write(cell('AC'), paciente.estado_civil.capitalize())
            else:
                sheet.write(cell('AC'), '')

            sheet.write(cell('AD'), paciente.etnia_nombre)
            seguros = []
            if paciente.seguro_sis:
                seguros.append('SIS')
            elif paciente.seguro_essalud:
                seguros.append('ESSALUD')
            elif paciente.seguro_privado:
                seguros.append('PRIVADO')
            elif paciente.seguro_sanidad:
                seguros.append('SANIDAD')
            else:
                seguros.append('OTROS')
            sheet.write(cell('AE'), seguros[0] if seguros else '')
            sheet.write(cell('AF'), paciente.componente.upper())
            sheet.write(cell('AG'), paciente.afiliacion.upper())
            sheet.write(cell('AH'), paciente.codigo_afiliacion)
            antecedentes_familiares = ['{}({})'.format(
                am.cie.nombre, ', '.join([
                    rel.nombre for rel in am.relaciones.all()
                    ])) for am in paciente.antecedentes_familiares.all()]

            if antecedentes_familiares:
                sheet.write(cell('AI'), ', '.join(antecedentes_familiares))
            else:
                sheet.write(cell('AI'), 'Niega')

            antecedentes_medicos = [
                am.cie.nombre for am in paciente.antecedentes_medicos.all()]

            if antecedentes_medicos:
                sheet.write(cell('AJ'), ', '.join(antecedentes_medicos))
            else:
                sheet.write(cell('AJ'), 'Niega')

            ultima_gestacion = paciente.ultimos_embarazos.all().order_by(
                'numero').first()
            if ultima_gestacion:
                sheet.write_datetime(
                    cell('AK'), ultima_gestacion.bebes.first().fecha)
            sheet.write(cell('AL'), ao.gestaciones)
            sheet.write(cell('AM'), ao.abortos)
            sheet.write(cell('AN'), ao.partos)
            sheet.write(cell('AO'), ao.vaginales)
            sheet.write(cell('AP'), ao.cesareas)
            sheet.write(cell('AQ'), ao.nacidos_vivos)
            sheet.write(cell('AR'), ao.nacidos_muertos)
            sheet.write(cell('AS'), ao.viven)
            sheet.write(cell('AT'), ao.muertos_menor_una_sem)
            sheet.write(cell('AU'), ao.muertos_mayor_igual_1sem)
            sheet.write(cell('AV'), 'Si' if ao.gestaciones in (0, 3) else 'No')
            sheet.write(cell('AW'), ao.nacidos_menor_2500g)
            sheet.write(cell('AX'), ao.embarazos_multiples)
            sheet.write(cell('AY'), ao.nacidos_menor_37sem)
            sheet.write(cell('AZ'), ao.viven)
            sheet.write(cell('BA'), ag.edad_menarquia)
            sheet.write(cell('BB'), ag.andria)
            sheet.write(cell('BC'), ag.edad_primera_relacion_sexual)
            sheet.write(
                cell('BD'), 'Regular' if ag.regimen_regular else 'Irregular')
            sheet.write(cell('BE'), ag.duracion_menstruacion)
            sheet.write(cell('BF'), ag.ciclo_menstruacion)

            sheet.write(cell('BG'), 'SI' if ag.tiene_papanicolaou else 'No')
            if ag.fecha_ultimo_papanicolaou:
                sheet.write_datetime(cell('BH'), ag.fecha_ultimo_papanicolaou)
            else:
                sheet.write(cell('BH'), '')

            if ag.resultado_papanicolaou:
                sheet.write(cell('BI'), ag.resultado_papanicolaou.upper())
            else:
                sheet.write(cell('BI'), '')

            sheet.write(cell('BJ'), ag.lugar_papanicolaou)
            metodos_anticonceptivos = []
            if ag.condon:
                metodos_anticonceptivos.append('Condon')
            if ag.ovulos:
                metodos_anticonceptivos.append('Ovulos')
            if ag.diu:
                metodos_anticonceptivos.append('DIU')
            if ag.inyectable or ag.inyectable_2:
                metodos_anticonceptivos.append('Inyectable')
            if ag.pastilla:
                metodos_anticonceptivos.append('Pastilla')
            if ag.implanon:
                metodos_anticonceptivos.append('Implanon')
            if ag.natural:
                metodos_anticonceptivos.append('Natural')

            if metodos_anticonceptivos:
                sheet.write(cell('BK'), ', '.join(metodos_anticonceptivos))
            else:
                sheet.write(cell('BK'), '')

            sheet.write(cell('BL'), 'SI' if ag.embarazo_mac else 'NO')
            if hasattr(paciente, 'vacuna') and paciente.vacuna:
                vacuna = paciente.vacuna
                sheet.write(cell('BM'), si_no_na(vacuna.rubeola))
                sheet.write(cell('BN'), si_no_na(vacuna.hepatitis_b))
                sheet.write(cell('BO'), si_no_na(vacuna.papiloma))
                sheet.write(cell('BP'), si_no_na(vacuna.fiebre_amarilla))
                sheet.write(
                    cell('BQ'), vacuna.antitetanica_numero_dosis_previas)
                sheet.write(
                    cell('BR'), vacuna.antitetanica_primera_dosis_valor)
                sheet.write(
                    cell('BS'), vacuna.antitetanica_segunda_dosis_valor)
                sheet.write(
                    cell('BT'), vacuna.antitetanica_tercera_dosis_valor)
            sheet.write(cell('BU'), embarazo.padre)
            if embarazo.fum:
                sheet.write_datetime(cell('BV'), embarazo.fum)
            else:
                sheet.write(cell('BV'), '')
            sheet.write(cell('BW'), si_no_na(embarazo.fum_confiable))
            sheet.write(cell('BX'), si_no_na(embarazo.captada))
            sheet.write(cell('BY'), si_no_na(embarazo.referida))
            sheet.write(cell('BZ'), embarazo.talla)
            sheet.write(cell('CA'), embarazo.peso)
            sheet.write(cell('CB'), embarazo.imc)
            sheet.write(cell('CC'), first_control.eg_fum)
            if embarazo.fecha_probable_parto_ultima_menstruacion:
                sheet.write_datetime(
                    cell('CD'),
                    embarazo.fecha_probable_parto_ultima_menstruacion)
            else:
                sheet.write(cell('CD'), '')
            if hasattr(embarazo, 'ficha_violencia_familiar') and \
                embarazo.ficha_violencia_familiar:
                ficha = embarazo.ficha_violencia_familiar

                if (ficha.violencia_fisica or ficha.violencia_psicologica or
                        ficha.violencia_sexual):
                    sheet.write(cell('CE'), 'SI')
                else:
                    sheet.write(cell('CE'), 'NO')

                agresores = []
                if ficha.violencia_fisica_agresores:
                    agresores.append(ficha.violencia_fisica_agresores)
                if ficha.violencia_psicologica_agresores:
                    agresores.append(ficha.violencia_psicologica_agresores)
                if ficha.violencia_sexual_agresores:
                    agresores.append(ficha.violencia_sexual_agresores)
                sheet.write(cell('CF'), ', '.join(agresores))
                sheet.write(cell('CG'), si_no_na(ficha.hematomas))
                sheet.write(cell('CH'), si_no_na(ficha.cicatrices))
                sheet.write(cell('CI'), si_no_na(ficha.laceraciones))
                sheet.write(cell('CJ'), si_no_na(ficha.quejas_cronicas))
                sheet.write(cell('CK'), si_no_na(ficha.cefalea))
                sheet.write(cell('CL'), si_no_na(ficha.problemas_apetito))
                sheet.write(cell('CM'), si_no_na(ficha.falta_de_confianza))
                sheet.write(cell('CN'), si_no_na(ficha.tristeza))
                sheet.write(cell('CO'), si_no_na(ficha.retraimiento))
                sheet.write(cell('CP'), si_no_na(ficha.llanto_frecuente))
                sheet.write(cell('CQ'), si_no_na(embarazo.usa_drogas))
            sheet.write(cell('CR'), si_no_na(embarazo.numero_cigarros_diarios))
            sheet.write(cell('CS'), embarazo.perdida_interes_placer or '')
            sheet.write(
                cell('CT'), embarazo.triste_deprimida_sin_esperanza or '')
            sheet.write(cell('CU'), embarazo.depresion_puntaje or '')
            if embarazo.fecha_tamizaje:
                sheet.write_datetime(cell('CV'), embarazo.fecha_tamizaje)
            else:
                sheet.write(cell('CV'), '')

            if hasattr(embarazo, 'ficha_problema') and embarazo.ficha_problema:
                ficha = embarazo.ficha_problema

                if ficha.poco_interes_o_placer:
                    sheet.write(
                        cell('CW'), ficha.poco_interes_o_placer.capitalize())
                else:
                    sheet.write(cell('CW'), '')

                if ficha.desanimada_deprimida:
                    sheet.write(
                        cell('CX'), ficha.desanimada_deprimida.capitalize())
                else:
                    sheet.write(cell('CX'), '')

                if ficha.problemas_dormir:
                    sheet.write(
                        cell('CY'), ficha.problemas_dormir.capitalize())
                else:
                    sheet.write(cell('CY'), '')

                if ficha.cansancio:
                    sheet.write(cell('CZ'), ficha.cansancio.capitalize())
                else:
                    sheet.write(cell('CZ'), '')

                if ficha.alimenticio:
                    sheet.write(cell('DA'), ficha.alimenticio.capitalize())
                else:
                    sheet.write(cell('DA'), '')

                if ficha.falta_autoestima:
                    sheet.write(
                        cell('DB'), ficha.falta_autoestima.capitalize())
                else:
                    sheet.write(cell('DB'), '')

                if ficha.dificultad_concentracion:
                    sheet.write(
                        cell('DC'),
                        ficha.dificultad_concentracion.capitalize())
                else:
                    sheet.write(cell('DC'), '')

                if ficha.mueve_lento_o_hiperactivo:
                    sheet.write(
                        cell('DD'),
                        ficha.mueve_lento_o_hiperactivo.capitalize())
                else:
                    sheet.write(cell('DD'), '')

                if ficha.pensamientos_autodestructivos:
                    sheet.write(
                        cell('DE'),
                        ficha.pensamientos_autodestructivos.capitalize())
                else:
                    sheet.write(cell('DE'), '')

                if ficha.difucultad_cumplir_labores:
                    sheet.write(
                        cell('DF'),
                        ficha.difucultad_cumplir_labores.capitalize())
                else:
                    sheet.write(cell('DF'), '')

                sheet.write(cell('DG'), ficha.puntaje or '')

            sheet.write(cell('DH'), si_no_na(embarazo.hospitalizacion))
            if embarazo.hospitalizacion_fecha:
                sheet.write_datetime(
                    cell('DI'), embarazo.hospitalizacion_fecha)
            else:
                sheet.write(cell('DI'), '')
            sheet.write(
                cell('DJ'), ', '.join([cie.nombre for cie in embarazo.hospitalizacion_diagnosticos.all()]))
            sheet.write(cell('DK'), si_no_na(embarazo.emergencia))
            if embarazo.emergencia_fecha:
                sheet.write(cell('DL'), embarazo.emergencia_fecha)
            else:
                sheet.write(cell('DL'), '')
            sheet.write(
                cell('DM'), ', '.join([
                                          cie.nombre for cie in
                                          embarazo.emergencia_diagnosticos.all()]))

            # ecografias
            eco_columns = ('DN', 'DO', 'DP', 'DQ', 'DR', 'DS')
            _counter = 0
            for eco in embarazo.ecografias.all()[:3]:
                if eco.fecha:
                    sheet.write(cell(eco_columns[_counter]), eco.fecha)
                else:
                    sheet.write(cell(eco_columns[_counter]), '')
                sheet.write(
                    cell(eco_columns[_counter + 1]),
                    eco.edad_gestacional_actual)
                _counter += 2
            column = 'DS'

            def get_column():
                def _next(v):
                    return 'A' if v == 'Z' else chr(ord(v) + 1)

                def _evaluate(v):
                    if v:
                        if v[0] == 'Z':
                            return 'A' + _evaluate(v[1:])
                        else:
                            return _next(v[0]) + v[1:]
                    else:
                        return 'A'

                return _evaluate(column[::-1])[::-1]

            last_control = controles.last()
            if hasattr(last_control, 'laboratorio') and \
                last_control.laboratorio:
                lab = last_control.laboratorio
                column = get_column()
                sheet.write(cell(column), lab.rapida_sifilis.upper())
                column = get_column()
                sheet.write(cell(column), lab.rapida_sifilis_2.upper())
                column = get_column()
                sheet.write(cell(column), lab.rapida_vih_1.upper())
                column = get_column()
                sheet.write(cell(column), lab.rapida_vih_2.upper())
                column = get_column()
                sheet.write(cell(column), upper_value(lab.grupo))
                column = get_column()
                sheet.write(cell(column), upper_value(lab.factor))
                column = get_column()
                sheet.write(cell(column), si_no_na(lab.rapida_hemoglobina))
                column = get_column()
                sheet.write(cell(column), lab.hemoglobina_1_resultado)
                column = get_column()
                sheet.write(cell(column), lab.hemoglobina_2_resultado)
                column = get_column()
                sheet.write(cell(column), lab.hemoglobina_alta_resultado)
                column = get_column()
                sheet.write(cell(column), upper_value(lab.glicemia_1))
                column = get_column()
                sheet.write(cell(column), upper_value(lab.glicemia_2))
                column = get_column()
                sheet.write(
                    cell(column), upper_value(lab.examen_completo_orina_1))
                column = get_column()
                sheet.write(
                    cell(column), upper_value(lab.examen_completo_orina_2))
                column = get_column()
                sheet.write(cell(column), upper_value(lab.leucocituria))
                column = get_column()
                sheet.write(cell(column), upper_value(lab.nitritos))
                column = get_column()
                sheet.write(cell(column), upper_value(lab.vdrl_rp_1))
                column = get_column()
                sheet.write(cell(column), upper_value(lab.vdrl_rp_2))
                column = get_column()
                sheet.write(cell(column), upper_value(lab.elisa))
                column = get_column()
                sheet.write(cell(column), upper_value(lab.pap))
                column = get_column()
                sheet.write(cell(column), upper_value(lab.iva))
                column = get_column()
                sheet.write(cell(column), lab.colposcopia.upper())
                column = get_column()
                sheet.write(cell(column), lab.ifi_western_blot.upper())
                column = get_column()
                sheet.write(cell(column), lab.htlv_1.upper())
                column = get_column()
                sheet.write(cell(column), lab.torch.upper())
                column = get_column()
                sheet.write(cell(column), lab.gota_gruesa.upper())
                column = get_column()
                sheet.write(cell(column), lab.malaria_prueba_rapida.upper())
                column = get_column()
                sheet.write(cell(column), lab.fluorencia_malaria.upper())
                column = get_column()
                sheet.write(cell(column), lab.urocultivo.upper())
                column = get_column()
                sheet.write(cell(column), lab.bk_en_esputo.upper())
                column = get_column()
                sheet.write(cell(column), lab.listeria.upper())
                column = get_column()
                sheet.write(cell(column), lab.tamizaje_hepatitis_b.upper())
                column = get_column()
                sheet.write(cell(column), lab.tolerancia_glucosa.upper())
                column = get_column()
                sheet.write(cell(column), lab.fta_abs.upper())
                column = get_column()
                sheet.write(cell(column), lab.tpha.upper())
            else:
                for i in range(35):
                    global column
                    column = get_column()

            for control in controles.all()[:10]:
                column = get_column()
                sheet.write(cell(column), control.establecimiento.nombre)
                column = get_column()
                sheet.write(cell(column), control.created_by.get_full_name())
                column = get_column()
                sheet.write_datetime(cell(column), control.atencion_fecha)
                column = get_column()
                sheet.write(cell(column), control.peso)
                column = get_column()
                sheet.write(cell(column), control.imc)
                column = get_column()
                sheet.write(cell(column), control.get_eg())
                column = get_column()
                if control.fecha_probable_parto:
                    sheet.write_datetime(
                        cell(column), control.fecha_probable_parto)
                else:
                    sheet.write(cell(column), '')

                column = get_column()
                sheet.write(cell(column), control.temperatura)
                column = get_column()
                sheet.write(cell(column), control.presion_arterial)
                column = get_column()
                sheet.write(cell(column), control.pulso)
                column = get_column()
                sheet.write(cell(column), control.frecuencia_respiratoria)
                column = get_column()
                sheet.write(cell(column), control.altura_uterina)
                column = get_column()
                sheet.write(cell(column), control.fcf)
                column = get_column()
                sheet.write(cell(column), upper_value(control.situacion))
                column = get_column()
                sheet.write(cell(column), upper_value(control.presentacion))
                column = get_column()
                sheet.write(cell(column), upper_value(control.posicion))
                column = get_column()
                sheet.write(
                    cell(column), upper_value(control.movimientos_fetales))
                column = get_column()
                sheet.write(
                    cell(column), upper_value(control.dinamica_uterina))
                column = get_column()
                sheet.write(
                    cell(column), upper_value(control.proteinuria_cualitativa))
                column = get_column()
                sheet.write(cell(column), upper_value(control.edemas))
                column = get_column()
                sheet.write(cell(column), upper_value(control.reflejos))
                column = get_column()
                sheet.write(cell(column), upper_value(control.examen_pezon))
                column = get_column()
                sheet.write(cell(column), control.indicacion_hierro)
                column = get_column()
                sheet.write(cell(column), control.indicacion_calcio)
                column = get_column()
                sheet.write(cell(column), control.indicacion_acido_folico)
                column = get_column()
                sheet.write(
                    cell(column), control.indicacion_hierro_acido_folico)
                column = get_column()
                sheet.write(
                    cell(column), upper_value(control.perfil_biofisico))
                column = get_column()
                if control.proxima_cita:
                    sheet.write_datetime(cell(column), control.proxima_cita)
                else:
                    sheet.write(cell(column), '')
                column = get_column()
                sheet.write(cell(column), control.numero_formato_sis)
                column = get_column()
                orientaciones = []
                if control.oc_planificacion_familiar:
                    orientaciones.append('Planificación familiar')
                if control.oc_lactancia_materna:
                    orientaciones.append('Lactancia Materna')
                if control.oc_its:
                    orientaciones.append('ITS')
                if control.oc_nutricion:
                    orientaciones.append('Nutrición')
                if control.oc_inmunizaciones:
                    orientaciones.append('Inmunizaciones')
                if control.oc_vih:
                    orientaciones.append('VIH')
                if control.oc_tbc:
                    orientaciones.append('TBC')
                sheet.write(cell(column), ', '.join(orientaciones))
                column = get_column()
                sheet.write(
                    cell(column), ', '.join([
                                                s.cie.nombre_display for s in control.sintomas.all()]))
                if hasattr(control, 'examen_fisico') and control.examen_fisico:
                    ef = control.examen_fisico
                    column = get_column()
                    sheet.write(cell(column), ef.piel_y_mucosas.upper())
                    column = get_column()
                    sheet.write(cell(column), ef.mamas.upper())
                    column = get_column()
                    sheet.write(cell(column), ef.respiratorio.upper())
                    column = get_column()
                    sheet.write(cell(column), ef.cardiovascular.upper())
                    column = get_column()
                    sheet.write(cell(column), ef.odontologico.upper())
                    column = get_column()
                    sheet.write(cell(column), ef.abdomen.upper())
                    column = get_column()
                    sheet.write(cell(column), ef.urinario.upper())
                    column = get_column()
                    sheet.write(cell(column), ef.neurologico.upper())
                    column = get_column()
                    sheet.write(cell(column), ef.nivel_conciencia.upper())
                    column = get_column()
                    sheet.write(cell(column), ef.especuloscopia_vagina.upper())
                    column = get_column()
                    sheet.write(cell(column), ef.especuloscopia_cervix.upper())
                    column = get_column()
                    sheet.write(
                        cell(column), ef.especuloscopia_fondo_de_saco.upper())
                    column = get_column()
                    sheet.write(cell(column), ef.especuloscopia_observaciones)
                    column = get_column()
                    sheet.write(
                        cell(column), si_no_na(ef.tv_cambio_cervicales))
                    column = get_column()
                    sheet.write(cell(column), ef.tv_vagina.upper())
                    column = get_column()
                    sheet.write(cell(column), ef.tv_utero.upper())
                    column = get_column()
                    sheet.write(cell(column), ef.tv_hallazgos.upper())
                    column = get_column()
                    sheet.write(cell(column), ef.tv_incorporacion.upper())
                    column = get_column()

                    if ef.tv_liquido_amniotico:
                        sheet.write(
                            cell(column), ef.tv_liquido_amniotico.upper())
                    else:
                        sheet.write(cell(column), '')

                    column = get_column()
                    sheet.write(cell(column), ef.tv_membranas.upper())
                    column = get_column()
                    sheet.write(cell(column), ef.tv_otros.upper())
                    column = get_column()
                    sheet.write(cell(column), ef.tv_tb_resultado)
                    column = get_column()
                    sheet.write(cell(column), ef.eg_dolor.upper())
                    column = get_column()
                    sheet.write(cell(column), ef.eg_posicion.upper())
                    column = get_column()
                    sheet.write(cell(column), ef.eg_restos.upper())
                    column = get_column()
                    sheet.write(cell(column), si_no_na(ef.eg_culdocentesis))
                    column = get_column()
                    sheet.write(cell(column), ef.eg_fondo_de_saco.upper())
                    column = get_column()
                    sheet.write(cell(column), si_no_na(ef.eg_mal_olor))
                    column = get_column()
                    sheet.write(cell(column), ef.eg_vulvas.upper())
                    column = get_column()
                    sheet.write(cell(column), ef.eg_genitales_externos.upper())
                    column = get_column()
                    sheet.write(cell(column), ef.eg_vagina.upper())
                else:
                    for i in range(31):
                        global column
                        column = get_column()
                if hasattr(control, 'diagnostico') and control.diagnostico:
                    dx = control.diagnostico
                    column = get_column()
                    sheet.write(
                        cell(column), ', '.join(['{}: {}'.format(
                            detalle.tipo.upper(), detalle.cie.codigo) for detalle in dx.detalles.all()]))
                    column = get_column()
                    sheet.write(cell(column), dx.plan_trabajo.upper())
                    column = get_column()
                    sheet.write(cell(column), dx.examenes_a_pedir)
                else:
                    for i in range(3):
                        global column
                        column = get_column()
                column = get_column()
                if control.psicoprofilaxis_fecha_1:
                    sheet.write_datetime(
                        cell(column), control.psicoprofilaxis_fecha_1)
                else:
                    sheet.write_blank(cell(column), '')
                column = get_column()
                if control.psicoprofilaxis_fecha_2:
                    sheet.write_datetime(
                        cell(column), control.psicoprofilaxis_fecha_2)
                else:
                    sheet.write_blank(cell(column), '')
                column = get_column()
                if control.psicoprofilaxis_fecha_3:
                    sheet.write_datetime(
                        cell(column), control.psicoprofilaxis_fecha_3)
                else:
                    sheet.write_blank(cell(column), '')
                column = get_column()
                if control.psicoprofilaxis_fecha_4:
                    sheet.write_datetime(
                        cell(column), control.psicoprofilaxis_fecha_4)
                else:
                    sheet.write_blank(cell(column), '')
                column = get_column()
                if control.psicoprofilaxis_fecha_5:
                    sheet.write_datetime(
                        cell(column), control.psicoprofilaxis_fecha_5)
                else:
                    sheet.write_blank(cell(column), '')
                column = get_column()
                if control.psicoprofilaxis_fecha_6:
                    sheet.write_datetime(
                        cell(column), control.psicoprofilaxis_fecha_6)
                else:
                    sheet.write_blank(cell(column), '')
                ic_fields = (
                    'ic_psicologia', 'ic_medicina', 'ic_nutricion',
                    'ic_odontologia', 'ic_enfermeria', 'ic_laboratorio',
                    'ic_ecografia',)
                for ic_f in ic_fields:
                    _field = getattr(control, ic_f)
                    if _field:
                        for i in range(1, 4):
                            column = get_column()
                            date_field = getattr(
                                control, '{}_fecha_{}'.format(ic_f, i))
                            if date_field:
                                sheet.write_datetime(cell(column), date_field)
                            else:
                                sheet.write_blank(cell(column), '')
                    else:
                        for i in range(3):
                            column = get_column()
                            sheet.write_blank(cell(column), '')
            if hasattr(embarazo, 'plan_parto') and embarazo.plan_parto:
                pp = embarazo.plan_parto
                if pp.e1_fecha:
                    sheet.write_datetime(cell('AOM'), pp.e1_fecha)
                else:
                    sheet.write(cell('AOM'), '')
                sheet.write(cell('AON'), pp.e1_distancia_tiempo_llegada)

                if pp.e1_se_quedara_todo_el_embarazo_en_domicilio_actual:
                    sheet.write(cell('AOO'), 'SI')
                else:
                    sheet.write(cell('AOO'), 'NO')

                sheet.write(cell('AOP'), upper_value(pp.e1_lugar_atencion))
                sheet.write(cell('AOQ'), pp.e1_lugar_atencion_razon_eleccion)
                if pp.e2_fecha:
                    sheet.write_datetime(cell('AOR'), pp.e2_fecha)
                else:
                    sheet.write(cell('AOR'), '')
                sheet.write(cell('AOS'), pp.e2_edad_gestacional)
                sheet.write(cell('AOT'), upper_value(pp.e2_lugar_atencion))
                sheet.write(cell('AOU'), upper_value(pp.e2_posicion_parto))
                sheet.write(cell('AOV'), upper_value(pp.e2_transporte))
                sheet.write(cell('AOW'), pp.e2_tiempo_llegada_1)
                sheet.write(cell('AOX'), pp.e2_tiempo_llegada_1)
                sheet.write(
                    cell('AOY'), upper_value(
                        pp.e2_persona_que_acompania_en_el_parto))
                sheet.write(
                    cell('AOZ'), upper_value(
                        pp.e2_persona_cuidara_hijos_en_casa))
                sheet.write(cell('APA'), upper_value(pp.donador_1_nombre))
                sheet.write(cell('APB'), upper_value(pp.donador_1_tipo_sangre))
                sheet.write(cell('APC'), upper_value(pp.donador_1_domicilio))
                sheet.write(cell('APD'), upper_value(pp.donador_1_edad))
                sheet.write(cell('APE'), upper_value(pp.donador_1_parentesco))
                sheet.write(cell('APF'), upper_value(pp.donador_2_nombre))
                sheet.write(cell('APG'), upper_value(pp.donador_2_tipo_sangre))
                sheet.write(cell('APH'), upper_value(pp.donador_2_domicilio))
                sheet.write(cell('API'), upper_value(pp.donador_2_edad))
                sheet.write(cell('APJ'), upper_value(pp.donador_2_parentesco))

            if controles.exists():
                row_counter += 1
        return wb


class LibroRegistroDiarioSeguimientoGestantesReport(object):
    start_date = None
    end_date = None
    establecimiento_ids = []

    def __init__(self, start_date, end_date, establecimiento_ids):
        self.start_date = start_date
        self.end_date = end_date
        self.establecimiento_ids = establecimiento_ids

    def _get_queryset(self):
        ids = Control.objects.filter(
            establecimiento_id__in=self.establecimiento_ids,
            atencion_fecha__range=[self.start_date, self.end_date],
            embarazo__activo=True
        ).values_list('embarazo_id')
        ids = set(map(lambda x: x[0], ids))
        return Embarazo.objects.prefetch_related(
            'paciente', 'controles', 'ecografias').annotate(
            controles_quantity=Count('controles')).filter(
            id__in=list(ids), controles_quantity__gte=1).order_by(
            'created')

    def get_book(self, output):
        wb = xlsxwriter.Workbook(output, {
            'default_date_format': 'dd/mm/yyyy'
        })
        sheet = wb.add_worksheet('Hoja 1')
        sheet.set_landscape()

        def header_format(size):
            _format = wb.add_format({
                'align': 'center',
                'size': size,
                'valign': 'vcenter',
                'border': 1
            })
            _format.set_text_wrap()
            return _format

        sheet.merge_range(
            'A1:AL1',
            'Libro de Registro Diario de Seguimiento de Gestante- Puerpera',
            header_format(36))
        sheet.merge_range(
            'AM1:BJ1',
            'Libro de Registro Diario de Seguimiento de Gestante- Puerpera',
            header_format(36))
        sheet.merge_range('A2:B2', 'EE.SS', header_format(14))
        sheet.merge_range('A3:K3', 'Datos Personales', header_format(16))
        sheet.merge_range('L3:AL3', 'Atención prenatal', header_format(16))
        sheet.merge_range('AM3:AZ3', 'Atención prenatal', header_format(16))
        sheet.merge_range('BA3:BD4', 'Datos de parto', header_format(12))
        sheet.merge_range(
            'BE3:BI3', 'Atención de puerperio', header_format(12))
        sheet.merge_range('A4:A7', 'N', header_format(11))
        sheet.merge_range('B4:B7', 'Historia Clinica', header_format(11))
        sheet.merge_range('C4:C7', 'Apellidos y Nombres', header_format(11))
        sheet.merge_range('D4:D7', 'Edad', header_format(11))
        sheet.merge_range('E4:E7', 'Dirección', header_format(11))
        sheet.merge_range('F4:I4', 'Tipo de seguro', header_format(11))
        sheet.merge_range('F5:F7', 'SIS', header_format(11))
        sheet.merge_range('G5:G7', 'ESSALUD', header_format(11))
        sheet.merge_range('H5:H7', 'FF.AA.PP', header_format(11))
        sheet.merge_range('I5:I7', 'No tiene seguro', header_format(11))
        sheet.merge_range('J4:J7', 'Grado de intrucción', header_format(11))
        sheet.merge_range('K4:K7', 'Estado Civil', header_format(11))
        sheet.merge_range('L4:M4', 'Formula obstétrica', header_format(11))
        sheet.merge_range('L5:L7', 'G', header_format(11))
        sheet.merge_range('M5:M7', 'P', header_format(11))
        sheet.merge_range('N4:N7', 'FUR', header_format(11))
        sheet.merge_range('O4:O7', 'FPP', header_format(11))
        sheet.merge_range(
            'P4:T4', 'Examenes auxiliares basales', header_format(11))
        sheet.merge_range(
            'U4:V4', 'Dosis de vacuna antitetanica', header_format(11))
        sheet.merge_range('W4:X4', 'Control odontológico', header_format(11))
        sheet.merge_range('Y4:Z4', 'Plan de parto', header_format(11))
        sheet.merge_range('AA4:AB4', 'VGB', header_format(11))
        sheet.merge_range('AC4:AH4', 'Adm Fe +', header_format(11))
        sheet.merge_range(
            'AM4:AZ4', 'Seguimiento de las atenciones prenatales',
            header_format(26))
        sheet.merge_range(
            'P5:P7',
            'Grupo y RH,Glucosa, Urocultivo y /o Exam.Comp. De Orina (Fecha)',
            header_format(11))
        sheet.merge_range(
            'Q5:Q7', 'Tamizaje para Sífilis (prueba y fecha)',
            header_format(11))
        sheet.merge_range(
            'R5:R7', 'Tamizaje para VIH (prueba y fecha)', header_format(11))
        sheet.merge_range('S5:S7', 'Ecografia (fecha)', header_format(11))
        sheet.merge_range(
            'T5:T7', 'Ecografia (Observacion)', header_format(11))
        sheet.merge_range('U5:U7', '1', header_format(11))
        sheet.merge_range('V5:V7', '2', header_format(11))
        sheet.merge_range('W5:W7', '1er', header_format(11))
        sheet.merge_range('X5:X7', '2do', header_format(11))
        sheet.merge_range('Y5:Y7', '1ra entrevista (fecha)', header_format(11))
        sheet.merge_range('Z5:Z7', '2da entrevista (fecha)', header_format(11))
        sheet.merge_range('AA5:AA7', 'Tamizaje', header_format(11))
        sheet.merge_range('AB5:AB7', 'Detección', header_format(11))
        sheet.merge_range('AC5:AC6', 'Fecha', header_format(11))
        sheet.merge_range('AD5:AD6', 'Fecha', header_format(11))
        sheet.merge_range('AE5:AE6', 'Fecha', header_format(11))
        sheet.merge_range('AF5:AF6', 'Fecha', header_format(11))
        sheet.merge_range('AG5:AG6', 'Fecha', header_format(11))
        sheet.merge_range('AH5:AH6', 'Fecha', header_format(11))
        sheet.write('AC7', '1', header_format(11))
        sheet.write('AD7', '2', header_format(11))
        sheet.write('AE7', '3', header_format(11))
        sheet.write('AF7', '4', header_format(11))
        sheet.write('AG7', '5', header_format(11))
        sheet.write('AH7', '6', header_format(11))
        sheet.merge_range('AI5:AJ5', '1ra APN', header_format(11))
        sheet.merge_range('AK5:AL5', '2da APN', header_format(11))
        sheet.merge_range('AM5:AN5', '3ra APN', header_format(11))
        sheet.merge_range('AO5:AP5', '4ta APN', header_format(11))
        sheet.merge_range('AQ5:AR5', '5ta APN', header_format(11))
        sheet.merge_range('AS5:AT5', '6ta APN', header_format(11))
        sheet.merge_range('AU5:AV5', '7ma APN', header_format(11))
        sheet.merge_range('AW5:AX5', '8va APN', header_format(11))
        sheet.merge_range('AY5:AZ5', '9na APN', header_format(11))
        sheet.write('AI6', 'Fecha', header_format(11))
        sheet.write('AI7', 'EG', header_format(11))
        sheet.write('AJ6', 'Diagnostico', header_format(11))
        sheet.write('AJ7', 'Signos de alarma', header_format(11))
        sheet.write('AK6', 'Fecha', header_format(11))
        sheet.write('AK7', 'EG', header_format(11))
        sheet.write('AL6', 'Diagnostico', header_format(11))
        sheet.write('AL7', 'Signos de alarma', header_format(11))
        sheet.write('AM6', 'Fecha', header_format(11))
        sheet.write('AM7', 'EG', header_format(11))
        sheet.write('AN6', 'Diagnostico', header_format(11))
        sheet.write('AN7', 'Signos de alarma', header_format(11))
        sheet.write('AO6', 'Fecha', header_format(11))
        sheet.write('AO7', 'EG', header_format(11))
        sheet.write('AP6', 'Diagnostico', header_format(11))
        sheet.write('AP7', 'Signos de alarma', header_format(11))
        sheet.write('AQ6', 'Fecha', header_format(11))
        sheet.write('AQ7', 'EG', header_format(11))
        sheet.write('AR6', 'Diagnostico', header_format(11))
        sheet.write('AR7', 'Signos de alarma', header_format(11))
        sheet.write('AS6', 'Fecha', header_format(11))
        sheet.write('AS7', 'EG', header_format(11))
        sheet.write('AT6', 'Diagnostico', header_format(11))
        sheet.write('AT7', 'Signos de alarma', header_format(11))
        sheet.write('AU6', 'Fecha', header_format(11))
        sheet.write('AU7', 'EG', header_format(11))
        sheet.write('AV6', 'Diagnostico', header_format(11))
        sheet.write('AV7', 'Signos de alarma', header_format(11))
        sheet.write('AW6', 'Fecha', header_format(11))
        sheet.write('AW7', 'EG', header_format(11))
        sheet.write('AX6', 'Diagnostico', header_format(11))
        sheet.write('AX7', 'Signos de alarma', header_format(11))
        sheet.write('AY6', 'Fecha', header_format(11))
        sheet.write('AY7', 'EG', header_format(11))
        sheet.write('AZ6', 'Diagnostico', header_format(11))
        sheet.write('AZ7', 'Signos de alarma', header_format(11))
        sheet.merge_range('BA5:BC6', 'Lugar de parto', header_format(11))
        sheet.write('BA7', 'I', header_format(11))
        sheet.write('BB7', 'D', header_format(11))
        sheet.write('BC7', 'T', header_format(11))
        sheet.merge_range(
            'BD5:BD7', 'Fecha de parto (dd-mm-aa)', header_format(11))
        sheet.merge_range('BE4:BE7', '1ra atención (fecha)', header_format(11))
        sheet.merge_range('BF4:BF7', '2da atención (fecha)', header_format(11))
        sheet.merge_range(
            'BG4:BG7', 'Administración de sulfato ferroso (30 Tab)',
            header_format(11))
        sheet.merge_range('BH4:BH7', 'Método de PP.FF', header_format(11))
        sheet.merge_range(
            'BI4:BI7', 'Expedición o verificación de certificado de RN vivo',
            header_format(11))
        sheet.merge_range('BJ3:BJ7', 'Observaciones', header_format(16))

        i = 8
        counter = 1

        def detail_format(date=False):
            op = {
                'align': 'center',
                'size': 11,
                'valign': 'vcenter',
                'border': 1
            }
            if date:
                op['num_format'] = 'dd/mm/yyyy'
            _format = wb.add_format(op)
            _format.set_text_wrap()
            return _format

        for embarazo in self._get_queryset():
            last_control = embarazo.controles.all().order_by(
                '-atencion_fecha').first()
            last_eco = embarazo.ecografias.all().order_by('-fecha').first()

            def _cell(_c):
                return '{c}{r1}:{c}{r2}'.format(c=_c, r1=i, r2=i + 1)

            paciente = embarazo.paciente
            nombre_completo = '{} {} {}'.format(
                paciente.apellido_paterno, paciente.apellido_materno,
                paciente.nombres)
            sheet.merge_range(_cell('A'), counter, detail_format())
            sheet.merge_range(
                _cell('B'), get_hc(paciente, last_control.establecimiento),
                detail_format())
            sheet.merge_range(_cell('C'), nombre_completo, detail_format())
            sheet.merge_range(_cell('D'), paciente.edad, detail_format())
            sheet.merge_range(_cell('E'), paciente.direccion, detail_format())

            if paciente.seguro_sis:
                sheet.merge_range(_cell('F'), 'X', detail_format())
            else:
                sheet.merge_range(_cell('F'), '', detail_format())

            if paciente.seguro_essalud:
                sheet.merge_range(_cell('G'), 'X', detail_format())
            else:
                sheet.merge_range(_cell('G'), '', detail_format())

            if paciente.seguro_sanidad:
                sheet.merge_range(_cell('H'), 'X', detail_format())
            else:
                sheet.merge_range(_cell('H'), '', detail_format())

            if not (paciente.seguro_essalud or paciente.seguro_sis or
                    paciente.seguro_otros or paciente.seguro_privado or
                    paciente.seguro_sanidad):
                sheet.merge_range(_cell('I'), 'X', detail_format())
            else:
                sheet.merge_range(_cell('I'), '', detail_format())

            if paciente.estudio_nombre is not None:
                sheet.merge_range(
                    _cell('J'), paciente.estudio_nombre.upper(),
                    detail_format())
            else:
                sheet.merge_range(_cell('J'), '', detail_format())

            if paciente.estado_civil is not None:
                sheet.merge_range(
                    _cell('K'), paciente.estado_civil.upper(), detail_format())
            else:
                sheet.merge_range(_cell('K'), '', detail_format())

            ao = paciente.antecedente_obstetrico
            sheet.merge_range(_cell('L'), ao.gestaciones + 1, detail_format())
            tmp_ao = ao.nacidos_vivos
            tmp_ao += ao.nacidos_muertos
            tmp_ao -= ao.nacidos_menor_37sem
            sheet.merge_range(
                _cell('M'), '{}{}{}{}'.format(
                    tmp_ao, ao.nacidos_menor_37sem, ao.abortos, ao.viven),
                detail_format())
            sheet.merge_range(
                _cell('N'), embarazo.fum if embarazo.fum else '',
                detail_format(date=True))
            try:
                sheet.merge_range(
                    _cell('O'), datetime.strptime(
                        str(last_control.fecha_probable_parto),
                        '%Y-%m-%d').strftime(
                        '%m/%d/%y'), detail_format())
            except:
                sheet.merge_range(_cell('O'), '', detail_format())
            if hasattr(last_control, 'laboratorio'):
                lab = last_control.laboratorio
                _values = []
                if lab.glicemia_1 and lab.glicemia_1 != 'no se hizo':
                    _values.append(
                        'Glucosa: {}'.format(lab.glicemia_1.upper()))
                if lab.grupo or lab.factor:
                    _values.append(
                        'Grupo y RH: {} {}'.format(
                            lab.grupo if lab.grupo else '',
                            lab.factor if lab.factor else ''))
                if lab.urocultivo and lab.urocultivo == 'positivo':
                    _values.append(
                        'Urocultivo: {}'.format(lab.urocultivo.upper()))
                if lab.examen_completo_orina_1 and \
                        lab.examen_completo_orina_1 == 'positivo':
                    _values.append(
                        'Examen completo orina: {}'.format(
                            lab.examen_completo_orina_1.upper()))
                if lab.hemoglobina_1:
                    _values.append(
                        'Hemoglobina: {}'.format(lab.hemoglobina_1_resultado))
                sheet.merge_range(
                    _cell('P'), '\n'.join(_values), detail_format())
                sheet.merge_range(
                    _cell('Q'), '{} {}'.format(
                        lab.rapida_sifilis.upper() if
                        lab.rapida_sifilis else '',
                        lab.rapida_sifilis_fecha if
                        lab.rapida_sifilis_fecha else ''),
                    detail_format(date=True))
                sheet.merge_range(
                    _cell('R'), '{} {}'.format(
                        lab.rapida_vih_1.upper() if lab.rapida_vih_1 else '',
                        lab.rapida_vih_1_fecha if
                        lab.rapida_vih_1_fecha else ''),
                    detail_format(date=True))
            else:
                sheet.merge_range(_cell('P'), '', detail_format())
                sheet.merge_range(_cell('Q'), '', detail_format())
                sheet.merge_range(_cell('R'), '', detail_format())
            if last_eco:
                sheet.merge_range(
                    _cell('S'), last_eco.fecha if last_eco.fecha else '',
                    detail_format(date=True))
                sheet.merge_range(
                    _cell('T'),
                    last_eco.observacion if last_eco.observacion else '',
                    detail_format())
            else:
                sheet.merge_range(_cell('S'), '', detail_format())
                sheet.merge_range(_cell('T'), '', detail_format())

            try:
                vac = paciente.vacuna

                if vac.antitetanica_primera_dosis:
                    sheet.merge_range(
                        _cell('U'),
                        vac.antitetanica_primera_dosis_valor,
                        detail_format())
                else:
                    sheet.merge_range(_cell('U'), '', detail_format())

                if vac.antitetanica_segunda_dosis:
                    sheet.merge_range(
                        _cell('V'),
                        vac.antitetanica_segunda_dosis_valor,
                        detail_format())
                else:
                    sheet.merge_range(_cell('V'), '', detail_format())


            except paciente._meta.model.vacuna.RelatedObjectDoesNotExist as e:
                sheet.merge_range(_cell('U'), '', detail_format())
                sheet.merge_range(_cell('V'), '', detail_format())

            if last_control:
                if last_control.ic_odontologia_fecha_1:
                    sheet.merge_range(
                        _cell('W'), last_control.ic_odontologia_fecha_1,
                        detail_format())
                else:
                    sheet.merge_range(_cell('W'), '', detail_format())

                if last_control.ic_odontologia_fecha_2:
                    sheet.merge_range(
                        _cell('X'), last_control.ic_odontologia_fecha_2,
                        detail_format())
                else:
                    sheet.merge_range(_cell('X'), '', detail_format())
            else:
                sheet.merge_range(_cell('W'), '', detail_format())
                sheet.merge_range(_cell('X'), '', detail_format())

            if hasattr(embarazo, 'plan_parto'):
                if embarazo.plan_parto.e1_fecha:
                    sheet.merge_range(
                        _cell('Y'), embarazo.plan_parto.e1_fecha,
                        detail_format(date=True))
                else:
                    sheet.merge_range(_cell('Y'), '', detail_format(date=True))

                if embarazo.plan_parto.e2_fecha:
                    sheet.merge_range(
                        _cell('Z'), embarazo.plan_parto.e2_fecha,
                        detail_format(date=True))
                else:
                    sheet.merge_range(_cell('Z'), '', detail_format(date=True))
            else:
                sheet.merge_range(_cell('Y'), '', detail_format())
                sheet.merge_range(_cell('Z'), '', detail_format())
            if hasattr(embarazo, 'ficha_violencia_familiar'):
                ficha = embarazo.ficha_violencia_familiar

                if ficha.violencia_fisica is not None and \
                        ficha.violencia_psicologica is not None and \
                        ficha.violencia_sexual is not None:
                    tmp_opcion = 'SI'
                else:
                    tmp_opcion = 'NO'

                sheet.merge_range(_cell('AA'), tmp_opcion, detail_format())

                if ficha.violencia_fisica or ficha.violencia_psicologica or ficha.violencia_sexual:
                    tmp_opcion = 'SI'
                else:
                    tmp_opcion = 'NO'

                sheet.merge_range(_cell('AB'), tmp_opcion, detail_format())
            else:
                sheet.merge_range(_cell('AA'), '', detail_format())
                sheet.merge_range(_cell('AB'), '', detail_format())
            cells = ('AC', 'AD', 'AE', 'AF', 'AG', 'AH')
            controles_hierro = embarazo.controles.filter(
                Q(indicacion_hierro__gt=0) |
                Q(indicacion_hierro_acido_folico__gt=0))[:6]
            c = 0
            for control in controles_hierro:
                sheet.merge_range(
                    _cell(cells[c]), control.atencion_fecha,
                    detail_format(date=True))
                c += 1
            for x in range(6 - controles_hierro.count()):
                sheet.merge_range(_cell(cells[c]), '', detail_format())
                c += 1
            cells = (
                ('AI', 'AJ'),
                ('AK', 'AL'),
                ('AM', 'AN'),
                ('AO', 'AP'),
                ('AQ', 'AR'),
                ('AS', 'AT'),
                ('AU', 'AV'),
                ('AW', 'AX'),
                ('AY', 'AZ')
            )
            c = 0
            controles = embarazo.controles.all()[:9]
            controles_qty = 0
            for control in controles:
                if hasattr(control, 'diagnostico'):
                    diagnosticos = ', '.join([
                        dx.cie.codigo for dx in control.diagnostico.detalles.all()])
                else:
                    diagnosticos = ''
                signos_alarma = ', '.join([
                    s.cie.nombre_display for s in control.sintomas.all()])
                sheet.write_datetime(
                    '{}{}'.format(cells[c][0], i), control.atencion_fecha,
                    detail_format(date=True))
                sheet.write(
                    '{}{}'.format(cells[c][0], i + 1), control.get_eg(),
                    detail_format())
                sheet.write(
                    '{}{}'.format(cells[c][1], i), diagnosticos,
                    detail_format())
                sheet.write(
                    '{}{}'.format(cells[c][1], i + 1), signos_alarma,
                    detail_format())
                c += 1
                controles_qty += 1
            for x in range(9 - controles_qty):
                sheet.write('{}{}'.format(cells[c][0], i), '', detail_format())
                sheet.write(
                    '{}{}'.format(cells[c][0], i + 1), '', detail_format())
                sheet.write('{}{}'.format(cells[c][1], i), '', detail_format())
                sheet.write(
                    '{}{}'.format(cells[c][1], i + 1), '', detail_format())
                c += 1
            if last_control is not None and hasattr(last_control, 'diagnostico'):
                sheet.merge_range(
                    _cell('BJ'), last_control.diagnostico.plan_trabajo,
                    detail_format())
            else:
                sheet.merge_range(_cell('BJ'), '', detail_format())
            counter += 1
            i += 2  # increase th row position
        return wb


class GlobalReportParto(object):
    establecimiento_ids = None

    def __init__(self, establecimiento_ids, start_date, end_date):
        self.establecimiento_ids = establecimiento_ids
        self.start_date = start_date
        self.end_date = end_date
        super(GlobalReportParto, self).__init__()

    def get_queryset_parto(self):
        partogramas = Partograma.objects.select_related('paciente', 'ingreso', 'mediciones').filter(
            establecimiento_id__in=self.establecimiento_ids,
            created__range=[self.start_date, self.end_date + timedelta(days=1)])
        for partograma in partogramas:
            try:
                partograma.terminacion_embarazo = TerminacionEmbarazo.objects.get(ingreso_id=partograma.ingreso.id)
            except TerminacionEmbarazo.DoesNotExist:
                partograma.terminacion_embarazo = None
        return partogramas

    def get_book(self, output):
        wb = xlsxwriter.Workbook(output, {
            'default_date_format': 'dd/mm/yyyy'
        })
        sheet = wb.add_worksheet('Partos')
        header_format = wb.add_format()
        header_format.set_bg_color('yellow')
        header_format.set_border()
        hour_format = wb.add_format({'num_format': 'hh:mm AM/PM'})
        date_col_size = 10
        for _index in range(2000):
            sheet.set_column(_index, _index, date_col_size)
        headers = (
            ('A1', 'Ingreso_fecha'),
            ('B1', 'Establecimiento'),
            ('C1', 'HC'),
            ('D1', 'DNI'),
            ('E1', 'Apellido paterno'),
            ('F1', 'Apellido materno'),
            ('G1', 'Nombres'),
            ('H1', 'Edad'),
            ('I1', 'Fecha de nacimiento'),
            ('J1', 'Transfusion_sanguinea'),
            ('K1', 'DNI_Responsable'),
            ('L1', 'Nombre_resposable'),
            ('M1', 'Tipo_parentezco_responsable'),
            ('N1', 'Lugar_nacimiento_pais'),
            ('O1', 'Lugar_nacimiento_departamento'),
            ('P1', 'Lugar_nacimiento_provincia'),
            ('Q1', 'Departamento_residencia'),
            ('R1', 'Provincia_residencia'),
            ('S1', 'Distrito_residencia'),
            ('T1', 'Sector_residencia'),
            ('U1', 'Direccion_residencia'),
            ('V1', 'Telefono_casa'),
            ('W1', 'Celular'),
            ('X1', 'Operaror_celular'),
            ('Y1', 'Correo_electronico'),
            ('Z1', 'Educacion'),
            ('AA1', 'Años_aprobados'),
            ('AB1', 'Ocupacion'),
            ('AC1', 'Estado_civil'),
            ('AD1', 'Etnia'),
            ('AE1', 'Tipo_seguro'),
            ('AF1', 'Componente'),
            ('AG1', 'Afiliacion'),
            ('AH1', 'Codigo_afiliacion'),
            ('AI1', 'Antecedentes_familiares'),
            ('AJ1', 'Antecedentes_medicos'),
            ('AK1', 'Fecha_ultima_gestacion'),
            ('AL1', 'Embarazos_previos_gestas'),
            ('AM1', 'Embarazos_previos_abortos'),
            ('AN1', 'Embarazos_previos_partos'),
            ('AO1', 'Embarazos_previos_vaginales'),
            ('AP1', 'Embarazos_previos_edad_cesareas'),
            ('AQ1', 'Embarazos_previos_nacidos_vivos'),
            ('AR1', 'Embarazos_previos_nacidos_muertos'),
            ('AS1', 'Embarazos_previos_viven'),
            ('AT1', 'embarazos_previos_muertos_1ra_sem'),
            ('AU1', 'embarazos_previos_despues_1ra_sem'),
            ('AV1', 'embarazos_previos_0_3'),
            ('AW1', 'embarazos_previos_menor_2500g'),
            ('AX1', 'embarazos_previos_multiple'),
            ('AY1', 'embarazos_previos_menor_37sem'),
            ('AZ1', 'embarazos_previos_viven'),
            ('BA1', 'Menarquia_edad'),
            ('BB1', 'andria'),
            ('BC1', 'edad_1ra_relacion_sexual'),
            ('BD1', 'regimen_catameneal'),
            ('BE1', 'duracion_menstruacion'),
            ('BF1', 'ciclo_menstruacion'),
            ('BG1', 'Papanicolao'),
            ('BH1', 'fecha_papanicolao'),
            ('BI1', 'resultado_papanicolao'),
            ('BJ1', 'lugar_papanicolao'),
            ('BK1', 'ultimo_metodo_anticonceptivo'),
            ('BL1', 'embarazo_usando_MAC'),
            ('BM1', 'vacuna_rubeola'),
            ('BN1', 'vacuna_hepatitis'),
            ('BO1', 'vacuna_papiloma'),
            ('BP1', 'vacuna_fiebre_amarilla'),
            ('BQ1', 'vacuna_antitetanica_dosis'),
            ('BR1', 'antitetanica_1ra_dosis'),
            ('BS1', 'antitetanica_2da_dosis'),
            ('BT1', 'antitetanica_3ra_dosis'),)

        for _cell, value in headers:
            sheet.write(_cell, value, header_format)

        column = 'BT'

        def get_column():
            def _next(v):
                return 'A' if v == 'Z' else chr(ord(v) + 1)

            def _evaluate(v):
                if v:
                    if v[0] == 'Z':
                        return 'A' + _evaluate(v[1:])
                    else:
                        return _next(v[0]) + v[1:]
                else:
                    return 'A'

            return _evaluate(column[::-1])[::-1]

        mediciones_headers = (
            'Medición_{}_Solución',
            'Medición_{}_Tocolisis',
            'Medición_{}_Oxitocina',
            'Medición_{}_Goteo',
            'Medición_{}_Medicamentos',
            'Medición_{}_Orina_volumen',
            'Medición_{}_Orina_cetonas',
            'Medición_{}_Orina_proteinas',
            'Medición_{}_Observaciones',
            'Medición_{}_Presión_sistólica',
            'Medición_{}_Presión_diastólica',
            'Medición_{}_Pulso',
            'Medición_{}_Frecuencia_respiratoria',
            'Medición_{}_Temperatura',
            'Medición_{}_Feto (FCF)',
            'Medición_{}_Dinámica_uterina_frecuencia',
            'Medición_{}_Dinámica_uterina_duración',
            'Medición_{}_Dinámica_uterina_intensidad',
            'Medición_{}_Moldeamientos',
            'Medición_{}_Tacto_vaginal_dilatación',
            'Medición_{}_Tacto_vaginal_incorporación',
            'Medición_{}_Descenso_cefálico',
            'Medición_{}_Membranas',
            'Medición_{}_Membranas_tipo',
            'Medición_{}_Membranas_tiempo',
            'Medición_{}_Líquido_amniótico',
            'Medición_{}_Variedad_presentacion',
            'Medición_{}_Variedad_presentacion',
            'Medición_{}_Encargado')

        for number in range(1, 13):
            for value in mediciones_headers:
                column = get_column()
                sheet.write('{}{}'.format(column, 1), value.format(number), header_format)

        cierre_headers = (
            'Fecha_cierre',
            'Hora_cierre',
            'Tipo_cierre',
            'Tiempo_duración_1er_periodo',
            'Inicio_1er_periodo',
            'Tiempo_duración_2do_periodo',
            'Inicio_2do_periodo',
            'Hora_1_2do_periodo',
            'Hora_2_2do_periodo',
            'Hora_3_2do_periodo',
            'Hora_4_2do_periodo',
            'Hora_5_2do_periodo',
            'Episiotomía',
            'Tipo_episitomía',
            'Desgarro',
            'Tipo_desgarro',
            'Tiempo_duración_3er_periodo',
            'Hora_3er_periodo',
            'Dirigido',
            'Sangrado aproximado'
        )

        for value in cierre_headers:
            column = get_column()
            sheet.write('{}{}'.format(column, 1), value, header_format)

        cierre_placenta_headers = (
            'Placenta_{}_desprendimiento',
            'Placenta_{}_Tipo',
            'Placenta_{}_Peso',
            'Placenta_{}_Ancho',
            'Placenta_{}_Longitud',
            'Placenta_{}_Otras_caracteristicas',
            'Membranas_{}',
            'Cordón_umbilical_{}_Longitud',
            'Cordón_umbilical_{}_Diametro',
            'Cordón_umbilical_{}_Inserción',
            'Cordón_umbilical_{}_Vasos',
            'Cordón_umbilical_{}_Circular',
            'Cordón_umbilical_{}_Circular_tipo',
            'Cordón_umbilical_{}_Otras_caracteristicas',
            'Líquido_amniótico_{}_Cantidad',
            'Líquido_amniótico_{}_Color',
            'Líquido_amniótico_{}_Olor',
            'Líquido_amniótico_{}_Otras_caracteristicas',
            'Anexo_{}_Otras_caracteristicas'
        )

        for number in range(1, 5):
            for value in cierre_placenta_headers:
                column = get_column()
                sheet.write('{}{}'.format(column, 1), value.format(number), header_format)

        row_counter = 2

        def cell(_column):
            return '{}{}'.format(_column, row_counter)

        def si_no_na(_value):
            if _value is None:
                return 'NA'
            elif _value:
                return 'SI'
            else:
                return 'NO'

        def upper_value(_value):
            if _value:
                return _value.upper()
            else:
                return ''

        for partograma in self.get_queryset_parto():
            paciente = partograma.paciente
            ag = paciente.antecedente_ginecologico
            ao = paciente.antecedente_obstetrico
            sheet.write_datetime(cell('A'), partograma.ingreso.fecha)
            sheet.write(cell('B'), partograma.establecimiento.nombre)
            sheet.write(
                cell('C'), get_hc(paciente, partograma.establecimiento)),
            sheet.write(cell('D'), paciente.numero_documento)
            sheet.write(cell('E'), paciente.apellido_paterno)
            sheet.write(cell('F'), paciente.apellido_materno)
            sheet.write(cell('G'), paciente.nombres)
            sheet.write(cell('H'), paciente.edad)
            sheet.write_datetime(cell('I'), paciente.fecha_nacimiento)
            sheet.write(
                cell('J'), 'SI' if paciente.transfusion_sanguinea else 'NO')
            sheet.write(cell('K'), paciente.dni_responsable)
            sheet.write(cell('L'), paciente.nombre_responsable)

            if paciente.tipo_parentesco_responsable is not None:
                sheet.write(
                    cell('M'), paciente.tipo_parentesco_responsable.upper())
            else:
                sheet.write(cell('M'), '')

            sheet.write(cell('N'), paciente.pais_nacimiento.nombre)

            if paciente.departamento_nacimiento is not None:
                sheet.write(cell('O'), paciente.departamento_nacimiento.nombre)
            else:
                sheet.write(cell('O'), '')

            if paciente.provincia_nacimiento is not None:
                sheet.write(cell('P'), paciente.provincia_nacimiento.nombre)
            else:
                sheet.write(cell('P'), '')

            sheet.write(cell('Q'), paciente.departamento_residencia.nombre)
            sheet.write(cell('R'), paciente.provincia_residencia.nombre)
            sheet.write(cell('S'), paciente.distrito_residencia.nombre)
            sheet.write(cell('T'), paciente.urbanizacion)
            sheet.write(cell('U'), paciente.direccion)
            sheet.write(cell('V'), paciente.telefono)
            sheet.write(cell('W'), paciente.celular or '')
            sheet.write(cell('X'), paciente.operador.capitalize())
            sheet.write(cell('Y'), paciente.email)
            sheet.write(cell('Z'), paciente.estudio_nombre.capitalize())
            sheet.write(cell('AA'), paciente.tiempo_estudio)
            sheet.write(cell('AB'), paciente.ocupacion_nombre)

            if paciente.estado_civil is not None:
                sheet.write(cell('AC'), paciente.estado_civil.capitalize())
            else:
                sheet.write(cell('AC'), '')

            sheet.write(cell('AD'), paciente.etnia_nombre)
            seguros = []
            if paciente.seguro_sis:
                seguros.append('SIS')
            elif paciente.seguro_essalud:
                seguros.append('ESSALUD')
            elif paciente.seguro_privado:
                seguros.append('PRIVADO')
            elif paciente.seguro_sanidad:
                seguros.append('SANIDAD')
            else:
                seguros.append('OTROS')
            sheet.write(cell('AE'), seguros[0] if seguros else '')
            sheet.write(cell('AF'), paciente.componente.upper())
            sheet.write(cell('AG'), paciente.afiliacion.upper())
            sheet.write(cell('AH'), paciente.codigo_afiliacion)
            antecedentes_familiares = ['{}({})'.format(
                am.cie.nombre, ', '.join([
                    rel.nombre for rel in am.relaciones.all()
                    ])) for am in paciente.antecedentes_familiares.all()]

            if antecedentes_familiares:
                sheet.write(cell('AI'), ', '.join(antecedentes_familiares))
            else:
                sheet.write(cell('AI'), 'Niega')

            antecedentes_medicos = [
                am.cie.nombre for am in paciente.antecedentes_medicos.all()]

            if antecedentes_medicos:
                sheet.write(cell('AJ'), ', '.join(antecedentes_medicos))
            else:
                sheet.write(cell('AJ'), 'Niega')

            ultima_gestacion = paciente.ultimos_embarazos.all().order_by(
                'numero').first()
            if ultima_gestacion:
                sheet.write_datetime(
                    cell('AK'), ultima_gestacion.bebes.first().fecha)
            sheet.write(cell('AL'), ao.gestaciones)
            sheet.write(cell('AM'), ao.abortos)
            sheet.write(cell('AN'), ao.partos)
            sheet.write(cell('AO'), ao.vaginales)
            sheet.write(cell('AP'), ao.cesareas)
            sheet.write(cell('AQ'), ao.nacidos_vivos)
            sheet.write(cell('AR'), ao.nacidos_muertos)
            sheet.write(cell('AS'), ao.viven)
            sheet.write(cell('AT'), ao.muertos_menor_una_sem)
            sheet.write(cell('AU'), ao.muertos_mayor_igual_1sem)
            sheet.write(cell('AV'), 'Si' if ao.gestaciones in (0, 3) else 'No')
            sheet.write(cell('AW'), ao.nacidos_menor_2500g)
            sheet.write(cell('AX'), ao.embarazos_multiples)
            sheet.write(cell('AY'), ao.nacidos_menor_37sem)
            sheet.write(cell('AZ'), ao.viven)
            sheet.write(cell('BA'), ag.edad_menarquia)
            sheet.write(cell('BB'), ag.andria)
            sheet.write(cell('BC'), ag.edad_primera_relacion_sexual)
            sheet.write(cell('BD'), 'Regular' if ag.regimen_regular else 'Irregular')
            sheet.write(cell('BE'), ag.duracion_menstruacion)
            sheet.write(cell('BF'), ag.ciclo_menstruacion)

            sheet.write(cell('BG'), 'SI' if ag.tiene_papanicolaou else 'No')
            if ag.fecha_ultimo_papanicolaou:
                sheet.write_datetime(cell('BH'), ag.fecha_ultimo_papanicolaou)
            else:
                sheet.write(cell('BH'), '')

            if ag.resultado_papanicolaou:
                sheet.write(cell('BI'), ag.resultado_papanicolaou.upper())
            else:
                sheet.write(cell('BI'), '')

            sheet.write(cell('BJ'), ag.lugar_papanicolaou)
            metodos_anticonceptivos = []
            if ag.condon:
                metodos_anticonceptivos.append('Condon')
            if ag.ovulos:
                metodos_anticonceptivos.append('Ovulos')
            if ag.diu:
                metodos_anticonceptivos.append('DIU')
            if ag.inyectable or ag.inyectable_2:
                metodos_anticonceptivos.append('Inyectable')
            if ag.pastilla:
                metodos_anticonceptivos.append('Pastilla')
            if ag.implanon:
                metodos_anticonceptivos.append('Implanon')
            if ag.natural:
                metodos_anticonceptivos.append('Natural')

            if metodos_anticonceptivos:
                sheet.write(cell('BK'), ', '.join(metodos_anticonceptivos))
            else:
                sheet.write(cell('BK'), '')

            sheet.write(cell('BL'), 'SI' if ag.embarazo_mac else 'NO')
            if hasattr(paciente, 'vacuna') and paciente.vacuna:
                vacuna = paciente.vacuna
                sheet.write(cell('BM'), si_no_na(vacuna.rubeola))
                sheet.write(cell('BN'), si_no_na(vacuna.hepatitis_b))
                sheet.write(cell('BO'), si_no_na(vacuna.papiloma))
                sheet.write(cell('BP'), si_no_na(vacuna.fiebre_amarilla))
                sheet.write(cell('BQ'), vacuna.antitetanica_numero_dosis_previas)
                sheet.write(cell('BR'), vacuna.antitetanica_primera_dosis_valor)
                sheet.write(cell('BS'), vacuna.antitetanica_segunda_dosis_valor)
                sheet.write(cell('BT'), vacuna.antitetanica_tercera_dosis_valor)

            column = 'BT'

            def get_column():
                def _next(v):
                    return 'A' if v == 'Z' else chr(ord(v) + 1)

                def _evaluate(v):
                    if v:
                        if v[0] == 'Z':
                            return 'A' + _evaluate(v[1:])
                        else:
                            return _next(v[0]) + v[1:]
                    else:
                        return 'A'

                return _evaluate(column[::-1])[::-1]

            def get_fcfs(fcfs):
                fcf_string = ''
                for fcf_m in fcfs:
                    fcf_string += str(fcf_m.fcf) + " "
                return fcf_string

            mediciones = partograma.mediciones.filter(
                fecha__range=[self.start_date, self.end_date])
            if mediciones:
                for medicion in mediciones:
                    column = get_column()
                    sheet.write(cell(column), medicion.solucion)
                    column = get_column()
                    sheet.write(cell(column), medicion.tocolisis)
                    column = get_column()
                    sheet.write(cell(column), medicion.oxitocina)
                    column = get_column()
                    sheet.write(cell(column), medicion.goteo)
                    column = get_column()
                    sheet.write(cell(column), medicion.medicamentos)
                    column = get_column()
                    sheet.write(cell(column), medicion.orina_volumen)
                    column = get_column()
                    sheet.write(cell(column), medicion.orina_cetona)
                    column = get_column()
                    sheet.write(cell(column), medicion.orina_proteinas)
                    column = get_column()
                    sheet.write(cell(column), medicion.observaciones)
                    column = get_column()
                    sheet.write(cell(column), medicion.presion_sistolica)
                    column = get_column()
                    sheet.write(cell(column), medicion.presion_diastolica)
                    column = get_column()
                    sheet.write(cell(column), medicion.pulso)
                    column = get_column()
                    sheet.write(cell(column), medicion.frecuencia_respiratoria)
                    column = get_column()
                    sheet.write(cell(column), medicion.temperatura)
                    fcfs = get_fcfs(ExamenFisicoFetal.objects.filter(medicion_parto=medicion))
                    if fcfs:
                        column = get_column()
                        sheet.write(cell(column), fcfs)
                    else:
                        global column
                        column = get_column()
                    column = get_column()
                    sheet.write(cell(column), medicion.du_frecuencia)
                    column = get_column()
                    sheet.write(cell(column), medicion.du_duracion)
                    column = get_column()
                    sheet.write(cell(column), medicion.du_intensidad)
                    column = get_column()
                    sheet.write(cell(column), medicion.moldeaminetos)
                    column = get_column()
                    sheet.write(cell(column), medicion.tv_dilatacion)
                    column = get_column()
                    sheet.write(cell(column), medicion.tv_incorporacion)
                    column = get_column()
                    sheet.write(cell(column), medicion.tv_descenso_cefalico)
                    column = get_column()
                    sheet.write(cell(column), medicion.tv_membranas)
                    column = get_column()
                    sheet.write(cell(column), medicion.tv_membranas_rotas_tipo)
                    column = get_column()
                    sheet.write(cell(column), medicion.tv_membranas_rotas_tiempo)
                    column = get_column()
                    sheet.write(cell(column), medicion.tv_liquido_amniotico)
                    column = get_column()
                    sheet.write(cell(column), medicion.tv_variedad_presentacion_val1)
                    column = get_column()
                    sheet.write(cell(column), medicion.tv_variedad_presentacion_val2)
                    column = get_column()
                    sheet.write(cell(column), medicion.created_by.get_full_name())
            else:
                for i in range(29):
                    global column
                    column = get_column()

            column = 'PD'
            # terminacion_embarazo = partograma.ingreso.terminacionembarazo
            terminacion = partograma.terminacion_embarazo
            if terminacion:
                column = get_column()
                sheet.write(cell(column), terminacion.fecha)
                column = get_column()
                sheet.write(cell(column), terminacion.hora, hour_format)
                column = get_column()
                sheet.write(cell(column), terminacion.tipo)
                hora_1 = terminacion.duracion_parto_perdiodo_1_horas if terminacion.duracion_parto_perdiodo_1_horas else ""
                minutos_1 = terminacion.duracion_parto_perdiodo_1_minutos if terminacion.duracion_parto_perdiodo_1_minutos else ""
                column = get_column()
                sheet.write(cell(column), '{}:{}'.format(hora_1, minutos_1))
                column = get_column()
                sheet.write(cell(column), terminacion.inicio_parto_periodo_1)
                hora_2 = terminacion.duracion_parto_perdiodo_2_horas if terminacion.duracion_parto_perdiodo_2_horas else ""
                minutos_2 = terminacion.duracion_parto_perdiodo_2_minutos if terminacion.duracion_parto_perdiodo_2_minutos else ""
                column = get_column()
                sheet.write(cell(column), '{}:{}'.format(hora_2, minutos_2))
                column = get_column()
                sheet.write(cell(column), terminacion.inicio_parto_periodo_2)
                column = get_column()
                sheet.write(cell(column), terminacion.hora_1_parto_periodo_2, hour_format)
                column = get_column()
                sheet.write(cell(column), terminacion.hora_2_parto_periodo_2, hour_format)
                column = get_column()
                sheet.write(cell(column), terminacion.hora_3_parto_periodo_2, hour_format)
                column = get_column()
                sheet.write(cell(column), terminacion.hora_4_parto_periodo_2, hour_format)
                column = get_column()
                sheet.write(cell(column), terminacion.hora_5_parto_periodo_2, hour_format)
                column = get_column()
                sheet.write(cell(column), terminacion.episiotomia)
                column = get_column()
                sheet.write(cell(column), terminacion.tipo_episiotomia)
                column = get_column()
                sheet.write(cell(column), terminacion.desgarro)
                column = get_column()
                sheet.write(cell(column), terminacion.desgarro_grado)
                hora_3 = terminacion.duracion_parto_perdiodo_3_horas if terminacion.duracion_parto_perdiodo_3_horas else ""
                minutos_3 = terminacion.duracion_parto_perdiodo_3_minutos if terminacion.duracion_parto_perdiodo_3_minutos else ""
                column = get_column()
                sheet.write(cell(column), '{}:{}'.format(hora_3, minutos_3))
                column = get_column()
                sheet.write(cell(column), terminacion.hora_parto_periodo_3, hour_format)
                column = get_column()
                sheet.write(cell(column), terminacion.dirigido_parto_periodo_3)
                column = get_column()
                sheet.write(cell(column), terminacion.sangrado_aproximado)

                if terminacion.placentas:
                    for placenta in terminacion.placentas.all():
                        column = get_column()
                        sheet.write(cell(column), placenta.placenta_desprendimiento)
                        column = get_column()
                        sheet.write(cell(column), placenta.placenta_tipo)
                        column = get_column()
                        sheet.write(cell(column), placenta.placenta_peso)
                        column = get_column()
                        sheet.write(cell(column), placenta.placenta_tamanio_ancho)
                        column = get_column()
                        sheet.write(cell(column), placenta.placenta_tamanio_longitud)
                        column = get_column()
                        sheet.write(cell(column), placenta.placenta_otras_caracteristicas)
                        column = get_column()
                        sheet.write(cell(column), placenta.membranas)
                        column = get_column()
                        sheet.write(cell(column), placenta.cordon_umbilical_longitud)
                        column = get_column()
                        sheet.write(cell(column), placenta.cordon_umbilical_diametro)
                        column = get_column()
                        sheet.write(cell(column), placenta.cordon_umbilical_insercion)
                        column = get_column()
                        sheet.write(cell(column), placenta.cordon_umbilical_vasos)
                        column = get_column()
                        sheet.write(cell(column), placenta.cordon_umbilical_circular)
                        column = get_column()
                        sheet.write(cell(column), placenta.cordon_umbilical_circular_tipo)
                        column = get_column()
                        sheet.write(cell(column), placenta.cordon_umbilical_otras_caracteristicas)
                        column = get_column()
                        sheet.write(cell(column), placenta.liquido_amniotico_cantidad)
                        column = get_column()
                        sheet.write(cell(column), placenta.liquido_amniotico_color)
                        column = get_column()
                        sheet.write(cell(column), placenta.liquido_amniotico_olor)
                        column = get_column()
                        sheet.write(cell(column), placenta.liquido_amniotico_otras_caracteristicas)
                        column = get_column()
                        sheet.write(cell(column), placenta.otras_caracteristicas)
                else:
                    for i in range(19):
                        global column
                        column = get_column()
            else:
                for i in range(20):
                    global column
                    column = get_column()

            row_counter += 1

        return wb


class GlobalReportPuerperio(object):
    establecimiento_ids = None

    def __init__(self, establecimiento_ids, start_date, end_date):
        self.establecimiento_ids = establecimiento_ids
        self.start_date = start_date
        self.end_date = end_date
        super(GlobalReportPuerperio, self).__init__()

    def get_queryset_puerperio(self):
        return TerminacionPuerpera.objects.prefetch_related('paciente', 'ingreso', 'terminacion_embarazo',
                                                            'monitoreo', 'diagnostico').filter(
            establecimiento_id__in=self.establecimiento_ids,
            created__range=[self.start_date, self.end_date])

    def get_book(self, output):
        wb = xlsxwriter.Workbook(output, {
            'default_date_format': 'dd/mm/yyyy'
        })
        sheet = wb.add_worksheet('Partos')
        header_format = wb.add_format()
        header_format.set_bg_color('yellow')
        header_format.set_border()
        hour_format = wb.add_format({'num_format': 'hh:mm AM/PM'})
        date_col_size = 10
        for _index in range(2000):
            sheet.set_column(_index, _index, date_col_size)
        headers = (
            ('A1', 'Puerperio fecha'),
            ('B1', 'Establecimiento'),
            ('C1', 'HC'),
            ('D1', 'DNI'),
            ('E1', 'Apellido paterno'),
            ('F1', 'Apellido materno'),
            ('G1', 'Nombres'),
            ('H1', 'Edad'),
            ('I1', 'Fecha de nacimiento'),
            ('J1', 'Transfusion_sanguinea'),
            ('K1', 'DNI_Responsable'),
            ('L1', 'Nombre_resposable'),
            ('M1', 'Tipo_parentezco_responsable'),
            ('N1', 'Lugar_nacimiento_pais'),
            ('O1', 'Lugar_nacimiento_departamento'),
            ('P1', 'Lugar_nacimiento_provincia'),
            ('Q1', 'Departamento_residencia'),
            ('R1', 'Provincia_residencia'),
            ('S1', 'Distrito_residencia'),
            ('T1', 'Sector_residencia'),
            ('U1', 'Direccion_residencia'),
            ('V1', 'Telefono_casa'),
            ('W1', 'Celular'),
            ('X1', 'Operaror_celular'),
            ('Y1', 'Correo_electronico'),
            ('Z1', 'Educacion'),
            ('AA1', 'Años_aprobados'),
            ('AB1', 'Ocupacion'),
            ('AC1', 'Estado_civil'),
            ('AD1', 'Etnia'),
            ('AE1', 'Tipo_seguro'),
            ('AF1', 'Componente'),
            ('AG1', 'Afiliacion'),
            ('AH1', 'Codigo_afiliacion'),
            ('AI1', 'Antecedentes_familiares'),
            ('AJ1', 'Antecedentes_medicos'),
            ('AK1', 'Fecha_ultima_gestacion'),
            ('AL1', 'Embarazos_previos_gestas'),
            ('AM1', 'Embarazos_previos_abortos'),
            ('AN1', 'Embarazos_previos_partos'),
            ('AO1', 'Embarazos_previos_vaginales'),
            ('AP1', 'Embarazos_previos_edad_cesareas'),
            ('AQ1', 'Embarazos_previos_nacidos_vivos'),
            ('AR1', 'Embarazos_previos_nacidos_muertos'),
            ('AS1', 'Embarazos_previos_viven'),
            ('AT1', 'embarazos_previos_muertos_1ra_sem'),
            ('AU1', 'embarazos_previos_despues_1ra_sem'),
            ('AV1', 'embarazos_previos_0_3'),
            ('AW1', 'embarazos_previos_menor_2500g'),
            ('AX1', 'embarazos_previos_multiple'),
            ('AY1', 'embarazos_previos_menor_37sem'),
            ('AZ1', 'embarazos_previos_viven'),
            ('BA1', 'Menarquia_edad'),
            ('BB1', 'Andria'),
            ('BC1', 'Edad_1ra_relacion_sexual'),
            ('BD1', 'Regimen_catameneal'),
            ('BE1', 'Duracion_menstruacion'),
            ('BF1', 'Ciclo_menstruacion'),
            ('BG1', 'Papanicolao'),
            ('BH1', 'Fecha_papanicolao'),
            ('BI1', 'Resultado_papanicolao'),
            ('BJ1', 'Lugar_papanicolao'),
            ('BK1', 'Último_metodo_anticonceptivo'),
            ('BL1', 'Embarazo_usando_MAC'),
            ('BM1', 'Vacuna_rubeola'),
            ('BN1', 'Vacuna_hepatitis'),
            ('BO1', 'Vacuna_papiloma'),
            ('BP1', 'Vacuna_fiebre_amarilla'),
            ('BQ1', 'Vacuna_antitetanica_dosis'),
            ('BR1', 'Antitetanica_1ra_dosis'),
            ('BS1', 'Antitetanica_2da_dosis'),
            ('BT1', 'Antitetanica_3ra_dosis'),
            ('BU1', 'Fecha_cierre'),
            ('BV1', 'Hora_cierre'),
            ('BW1', 'Egreso'),
            ('BX1', 'Control_de_puerperio'),
            ('BY1', 'Consejería_planificación_familiar'),
            ('BZ1', 'Consejería_nutricional'),
            ('CA1', 'Otras_medidas_profilácticas_especializadas'),
            ('CB1', 'Atención_y_examen_de_madre_en_periodo_de_lactancia'),
            ('CC1', 'Seguimiento_post_parto_de_rutina'),
            ('CD1', 'Anticonceptivo_Ligadura_turbia'),
            ('CE1', 'Anticonceptivo_Anticoncep._Combinada'),
            ('CF1', 'Anticonceptivo_Abstinencia_periodica'),
            ('CG1', 'Anticonceptivo_MELA'),
            ('CH1', 'Anticonceptivo_Solo_ori/consejo'),
            ('CI1', 'Anticonceptivo_Condón'),
            ('CJ1', 'Anticonceptivo_Progestag._inyectables'),
            ('CK1', 'Anticonceptivo_Ninguno'),
            ('CL1', 'Anticonceptivo_DIU'),
            ('CM1', 'Anticonceptivo_Progestag._orales'),
            ('CN1', 'Anticonceptivo_Otro'),
            ('CO1', 'Anticonceptivo_Observación'),
            ('CP1', 'Cita'),
            ('CQ1', 'Centro_de_salud_perteneciente'),
            ('CR1', 'Certificado_de_nacido_vivo'),
            )

        for _cell, value in headers:
            sheet.write(_cell, value, header_format)

        column = 'CR'

        def get_column():
            def _next(v):
                return 'A' if v == 'Z' else chr(ord(v) + 1)

            def _evaluate(v):
                if v:
                    if v[0] == 'Z':
                        return 'A' + _evaluate(v[1:])
                    else:
                        return _next(v[0]) + v[1:]
                else:
                    return 'A'

            return _evaluate(column[::-1])[::-1]

        monitoreo_headers = (
            'Monitoreo_{}_Fecha',
            'Monitoreo_{}_Hora',
            'Monitoreo_{}_Presion_sistolica',
            'Monitoreo_{}_Presion_diastolica',
            'Monitoreo_{}_Pulso',
            'Monitoreo_{}_Frecuencia_respiratoria',
            'Monitoreo_{}_Temperatura',
            'Monitoreo_{}_Mamas_pezón',
            'Monitoreo_{}_Mamas_características',
            'Monitoreo_{}_Utero_características',
            'Monitoreo_{}_Utero_ubicación',
            'Monitoreo_{}_Loquios_características',
            'Monitoreo_{}_Loquios_cantidad',
            'Monitoreo_{}_Loquios_olor',
            'Monitoreo_{}_Episeotomia_tipo',
            'Monitoreo_{}_Episeotomia_caracteristicas',
            'Monitoreo_{}_Vía_periférica',
            'Monitoreo_{}_Vía_periférica_tipo_de_solución',
            'Monitoreo_{}_Vía_periférica_oxitocina',
            'Monitoreo_{}_Vía_periférica_cantidad',
            'Monitoreo_{}_Hemoglobina_post_parto',
            'Monitoreo_{}_Fecha_hemoglobina',
            'Monitoreo_{}_Elisa',
            'Monitoreo_{}_Fecha_elisa',
            'Monitoreo_{}_RPR',
            'Monitoreo_{}_RPR_fecha',
            'Monitoreo_{}_Alojamiento_conjunto',
            'Monitoreo_{}_Alojamiento_conjunto_observación',
            'Monitoreo_{}_Contacto_piel',
            'Monitoreo_{}_Contacto_piel_observación')

        for number in range(1, 7):
            for value in monitoreo_headers:
                column = get_column()
                sheet.write(
                    '{}{}'.format(column, 1), value.format(number),
                    header_format)

        row_counter = 2

        def cell(_column):
            return '{}{}'.format(_column, row_counter)

        def si_no_na(_value):
            if _value is None:
                return 'NA'
            elif _value:
                return 'SI'
            else:
                return 'NO'

        def upper_value(_value):
            if _value:
                return _value.upper()
            else:
                return ''

        for puerperio in self.get_queryset_puerperio():
            paciente = puerperio.paciente
            ag = paciente.antecedente_ginecologico
            ao = paciente.antecedente_obstetrico
            sheet.write_datetime(cell('A'), puerperio.ingreso.fecha)
            sheet.write(cell('B'), puerperio.establecimiento.nombre)
            sheet.write(cell('C'), get_hc(paciente, puerperio.establecimiento)),
            sheet.write(cell('D'), paciente.numero_documento)
            sheet.write(cell('E'), paciente.apellido_paterno)
            sheet.write(cell('F'), paciente.apellido_materno)
            sheet.write(cell('G'), paciente.nombres)
            sheet.write(cell('H'), paciente.edad)
            sheet.write_datetime(cell('I'), paciente.fecha_nacimiento)
            sheet.write(cell('J'), 'SI' if paciente.transfusion_sanguinea else 'NO')
            sheet.write(cell('K'), paciente.dni_responsable)
            sheet.write(cell('L'), paciente.nombre_responsable)

            if paciente.tipo_parentesco_responsable is not None:
                sheet.write(cell('M'), paciente.tipo_parentesco_responsable.upper())
            else:
                sheet.write(cell('M'), '')

            sheet.write(cell('N'), paciente.pais_nacimiento.nombre)

            if paciente.departamento_nacimiento is not None:
                sheet.write(cell('O'), paciente.departamento_nacimiento.nombre)
            else:
                sheet.write(cell('O'), '')

            if paciente.provincia_nacimiento is not None:
                sheet.write(cell('P'), paciente.provincia_nacimiento.nombre)
            else:
                sheet.write(cell('P'), '')

            sheet.write(cell('Q'), paciente.departamento_residencia.nombre)
            sheet.write(cell('R'), paciente.provincia_residencia.nombre)
            sheet.write(cell('S'), paciente.distrito_residencia.nombre)
            sheet.write(cell('T'), paciente.urbanizacion)
            sheet.write(cell('U'), paciente.direccion)
            sheet.write(cell('V'), paciente.telefono)
            sheet.write(cell('W'), paciente.celular or '')
            sheet.write(cell('X'), paciente.operador.capitalize())
            sheet.write(cell('Y'), paciente.email)
            sheet.write(cell('Z'), paciente.estudio_nombre.capitalize())
            sheet.write(cell('AA'), paciente.tiempo_estudio)
            sheet.write(cell('AB'), paciente.ocupacion_nombre)

            if paciente.estado_civil is not None:
                sheet.write(cell('AC'), paciente.estado_civil.capitalize())
            else:
                sheet.write(cell('AC'), '')

            sheet.write(cell('AD'), paciente.etnia_nombre)
            seguros = []
            if paciente.seguro_sis:
                seguros.append('SIS')
            elif paciente.seguro_essalud:
                seguros.append('ESSALUD')
            elif paciente.seguro_privado:
                seguros.append('PRIVADO')
            elif paciente.seguro_sanidad:
                seguros.append('SANIDAD')
            else:
                seguros.append('OTROS')
            sheet.write(cell('AE'), seguros[0] if seguros else '')
            sheet.write(cell('AF'), paciente.componente.upper())
            sheet.write(cell('AG'), paciente.afiliacion.upper())
            sheet.write(cell('AH'), paciente.codigo_afiliacion)
            antecedentes_familiares = ['{}({})'.format(
                am.cie.nombre, ', '.join([
                    rel.nombre for rel in am.relaciones.all()
                    ])) for am in paciente.antecedentes_familiares.all()]

            if antecedentes_familiares:
                sheet.write(cell('AI'), ', '.join(antecedentes_familiares))
            else:
                sheet.write(cell('AI'), 'Niega')

            antecedentes_medicos = [
                am.cie.nombre for am in paciente.antecedentes_medicos.all()]

            if antecedentes_medicos:
                sheet.write(cell('AJ'), ', '.join(antecedentes_medicos))
            else:
                sheet.write(cell('AJ'), 'Niega')

            ultima_gestacion = paciente.ultimos_embarazos.all().order_by(
                'numero').first()
            if ultima_gestacion:
                sheet.write_datetime(
                    cell('AK'), ultima_gestacion.bebes.first().fecha)
            sheet.write(cell('AL'), ao.gestaciones)
            sheet.write(cell('AM'), ao.abortos)
            sheet.write(cell('AN'), ao.partos)
            sheet.write(cell('AO'), ao.vaginales)
            sheet.write(cell('AP'), ao.cesareas)
            sheet.write(cell('AQ'), ao.nacidos_vivos)
            sheet.write(cell('AR'), ao.nacidos_muertos)
            sheet.write(cell('AS'), ao.viven)
            sheet.write(cell('AT'), ao.muertos_menor_una_sem)
            sheet.write(cell('AU'), ao.muertos_mayor_igual_1sem)
            sheet.write(cell('AV'), 'Si' if ao.gestaciones in (0, 3) else 'No')
            sheet.write(cell('AW'), ao.nacidos_menor_2500g)
            sheet.write(cell('AX'), ao.embarazos_multiples)
            sheet.write(cell('AY'), ao.nacidos_menor_37sem)
            sheet.write(cell('AZ'), ao.viven)
            sheet.write(cell('BA'), ag.edad_menarquia)
            sheet.write(cell('BB'), ag.andria)
            sheet.write(cell('BC'), ag.edad_primera_relacion_sexual)
            sheet.write(
                cell('BD'), 'Regular' if ag.regimen_regular else 'Irregular')
            sheet.write(cell('BE'), ag.duracion_menstruacion)
            sheet.write(cell('BF'), ag.ciclo_menstruacion)

            sheet.write(cell('BG'), 'SI' if ag.tiene_papanicolaou else 'No')
            if ag.fecha_ultimo_papanicolaou:
                sheet.write_datetime(cell('BH'), ag.fecha_ultimo_papanicolaou)
            else:
                sheet.write(cell('BH'), '')

            if ag.resultado_papanicolaou:
                sheet.write(cell('BI'), ag.resultado_papanicolaou.upper())
            else:
                sheet.write(cell('BI'), '')

            sheet.write(cell('BJ'), ag.lugar_papanicolaou)
            metodos_anticonceptivos = []
            if ag.condon:
                metodos_anticonceptivos.append('Condon')
            if ag.ovulos:
                metodos_anticonceptivos.append('Ovulos')
            if ag.diu:
                metodos_anticonceptivos.append('DIU')
            if ag.inyectable or ag.inyectable_2:
                metodos_anticonceptivos.append('Inyectable')
            if ag.pastilla:
                metodos_anticonceptivos.append('Pastilla')
            if ag.implanon:
                metodos_anticonceptivos.append('Implanon')
            if ag.natural:
                metodos_anticonceptivos.append('Natural')

            if metodos_anticonceptivos:
                sheet.write(cell('BK'), ', '.join(metodos_anticonceptivos))
            else:
                sheet.write(cell('BK'), '')

            sheet.write(cell('BL'), 'SI' if ag.embarazo_mac else 'NO')
            if hasattr(paciente, 'vacuna') and paciente.vacuna:
                vacuna = paciente.vacuna
                sheet.write(cell('BM'), si_no_na(vacuna.rubeola))
                sheet.write(cell('BN'), si_no_na(vacuna.hepatitis_b))
                sheet.write(cell('BO'), si_no_na(vacuna.papiloma))
                sheet.write(cell('BP'), si_no_na(vacuna.fiebre_amarilla))
                sheet.write(cell('BQ'), vacuna.antitetanica_numero_dosis_previas)
                sheet.write(cell('BR'), vacuna.antitetanica_primera_dosis_valor)
                sheet.write(cell('BS'), vacuna.antitetanica_segunda_dosis_valor)
                sheet.write(cell('BT'), vacuna.antitetanica_tercera_dosis_valor)
                sheet.write(cell('BU'), puerperio.fecha)
                sheet.write(cell('BV'), puerperio.hora, hour_format)
                sheet.write(cell('BW'), puerperio.tipo)
                detalles = puerperio.detalles_puerperio.values_list('cie__codigo', flat=True)
                sheet.write(cell('BX'), "X" if '59430' in detalles else "")
                sheet.write(cell('BY'), "X" if '99402' in detalles else "")
                sheet.write(cell('BZ'), "X" if '99403' in detalles else "")
                sheet.write(cell('CA'), "X" if 'Z298' in detalles else "")
                sheet.write(cell('CB'), "X" if 'Z391' in detalles else "")
                sheet.write(cell('CC'), "X" if 'Z392' in detalles else "")
                sheet.write(cell('CD'), puerperio.ant_ligadura_tubaria)
                sheet.write(cell('CE'), puerperio.ant_anticoncec_combinada)
                sheet.write(cell('CF'), puerperio.ant_abstinencia_periodica)
                sheet.write(cell('CG'), puerperio.ant_mela)
                sheet.write(cell('CH'), puerperio.ant_solo_ori_consej)
                sheet.write(cell('CI'), puerperio.ant_condon)
                sheet.write(cell('CJ'), puerperio.ant_inyectables)
                sheet.write(cell('CK'), puerperio.ant_ninguno)
                sheet.write(cell('CL'), puerperio.ant_diu)
                sheet.write(cell('CM'), puerperio.ant_orales)
                sheet.write(cell('CN'), puerperio.ant_otro)
                sheet.write(cell('CO'), puerperio.ant_observaciones)
                sheet.write(cell('CP'), puerperio.control_puerperio)
                sheet.write(cell('CQ'), puerperio.centro_salud.nombre)
                sheet.write(cell('CR'), puerperio.certificado_nacido_vivo_numero)

            column = 'CR'

            def get_column():
                def _next(v):
                    return 'A' if v == 'Z' else chr(ord(v) + 1)

                def _evaluate(v):
                    if v:
                        if v[0] == 'Z':
                            return 'A' + _evaluate(v[1:])
                        else:
                            return _next(v[0]) + v[1:]
                    else:
                        return 'A'

                return _evaluate(column[::-1])[::-1]

            monitoreos = puerperio.monitoreo.mediciones.all()
            if monitoreos:
                for monitoreo in monitoreos:
                    column = get_column()
                    sheet.write(cell(column), monitoreo.fecha)
                    column = get_column()
                    sheet.write(cell(column), monitoreo.hora, hour_format)
                    column = get_column()
                    sheet.write(cell(column), monitoreo.presion_sistolica)
                    column = get_column()
                    sheet.write(cell(column), monitoreo.presion_diastolica)
                    column = get_column()
                    sheet.write(cell(column), monitoreo.pulso)
                    column = get_column()
                    sheet.write(cell(column), monitoreo.frecuencia_respiratoria)
                    column = get_column()
                    sheet.write(cell(column), monitoreo.temperatura)
                    column = get_column()
                    sheet.write(cell(column), monitoreo.mamas_pezon)
                    column = get_column()
                    sheet.write(cell(column), monitoreo.mamas_caracteristicas)
                    column = get_column()
                    sheet.write(cell(column), monitoreo.utero_caracteristicas)
                    column = get_column()
                    sheet.write(cell(column), monitoreo.utero_ubicacion)
                    column = get_column()
                    sheet.write(cell(column), monitoreo.loquios_caracteristicas)
                    column = get_column()
                    sheet.write(cell(column), monitoreo.loquios_cantidad)
                    column = get_column()
                    sheet.write(cell(column), monitoreo.loquios_olor)
                    column = get_column()
                    sheet.write(cell(column), monitoreo.episeotomia_tipo)
                    column = get_column()
                    sheet.write(cell(column), monitoreo.episeotomia_caracteristicas)
                    column = get_column()
                    sheet.write(cell(column), monitoreo.via_periferica)
                    column = get_column()
                    sheet.write(cell(column), monitoreo.vp_tipo_de_solucion)
                    column = get_column()
                    sheet.write(cell(column), monitoreo.vp_oxitocina)
                    column = get_column()
                    sheet.write(cell(column), monitoreo.vp_cantidad)
                    column = get_column()
                    sheet.write(cell(column), monitoreo.lab_hemoglobina_post_parto)
                    column = get_column()
                    sheet.write(cell(column), monitoreo.lab_fecha_hemoglobina)
                    column = get_column()
                    sheet.write(cell(column), monitoreo.lab_elisa)
                    column = get_column()
                    sheet.write(cell(column), monitoreo.lab_elisa_fecha)
                    column = get_column()
                    sheet.write(cell(column), monitoreo.lab_rpr)
                    column = get_column()
                    sheet.write(cell(column), monitoreo.lab_rpr_fecha)
                    column = get_column()
                    sheet.write(cell(column), monitoreo.alojamiento_conjunto)
                    column = get_column()
                    sheet.write(cell(column), monitoreo.alojamiento_conjunto_observacion)
                    column = get_column()
                    sheet.write(cell(column), monitoreo.contacto_piel)
                    column = get_column()
                    sheet.write(cell(column), monitoreo.contacto_piel_observacion)
            else:
                for i in range(30):
                    global column
                    column = get_column()

            row_counter += 1

        return wb
