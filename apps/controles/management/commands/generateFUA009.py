import subprocess
import requests
import os

from datetime import datetime
from optparse import make_option
from time import sleep
import csv

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.utils import timezone
from mpi_client.client import CiudadanoClient

from controles.models import Control, Laboratorio
from pacientes.models import HistoriaClinica
from establecimientos.models import Establecimiento



class Command(BaseCommand):
    help = 'Generar trama FUA 009'
    option_list = BaseCommand.option_list + (
        make_option(
            "-e",
            "--establecimiento",
            dest="establecimiento",
            help="Indica codigo renaes del establecimiento al que se esta generando el LOTE FUA",
            metavar="SLUG"
        ),
        make_option(
            "-d",
            "--date",
            dest="date",
            help="Indica la fecha de inicio del piloto - formato DD/MM/YYYY",
            metavar="SLUG"
        ),
        make_option(
            "-s",
            "--semana",
            dest="semana",
            help="Indica el dia de la semana que el proceso correra esta en base 0 [0:Lunes, ...., 6:Domingo]",
            metavar="SLUG"
        ),
    )

    def generar_diagnosticos(self, control):
        try:
            fila = []
            antecedentes = control.paciente.antecedente_obstetrico
            filas_afectadas = 1
            fila.append([
                control.id,  # Id Atencion
                "Z348" if antecedentes is not None and antecedentes.partos > 0 else "Z340",
                filas_afectadas,
                "I",
                "1"
            ])
            resultado = Laboratorio.objects.filter(paciente=control.paciente, hemoglobina_1_resultado__lte=10)
            if resultado.count() > 0:
                filas_afectadas += 1
                fila.append([
                    control.id,  # Id Atencion
                    "O990",
                    filas_afectadas,
                    "I",
                    "1"
                ])
            return fila, filas_afectadas
        except Exception as ex:
            self.stdout.write("Error en generar los diagnosticos asociados a la atencion: %s" % control.id)
            self.stderr.write(ex.message)
            return None, 0

    def generar_atencion(self, control):
        try:
            proxy = CiudadanoClient(settings.MPI_API_TOKEN)
            ciudadano = proxy.ver(control.paciente.numero_documento)
            if ciudadano['tipo_seguro'] != '2':
                # Obviar los registros que no son sis
                self.stdout.write("El paciente {0} de esta atencion {1} no cuenta con SIS activo:"
                                  .format(control.paciente.numero_documento, control.id))
                return None, 0, ""

            datos_sis = proxy.ver_datos_sis(ciudadano['uid'])
            establecimiento = control.establecimiento
            numerofua = establecimiento.fuas_numinicial + (
                establecimiento.fuas_incremento if establecimiento.fuas_incremento else 0)

            if numerofua >= establecimiento.fuas_numfinal:
                return None, 0, ""

            current_month = control.atencion_fecha.strftime('%m')
            current_year = control.atencion_fecha.strftime('%Y')

            fecha_nacimiento = ciudadano.get('fecha_nacimiento')
            if fecha_nacimiento:
                fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').strftime('%d/%m/%Y')

            fila = [
                control.id,  # Id Atencion (1)
                establecimiento.fuas_disa,  # Codigo DISA-SIS(Parametro de Configuracion de IPRESS) (2)
                timezone.now().strftime('%y'),  # Lote (3)
                str(numerofua).zfill(8),  # Numero de Formato FUA por Establecimiento (4)
                establecimiento.fuas_udr,  # Codigo UDR Catatogo SIS (Parametro de Configuracion de IPRESS) (5)
                str(control.establecimiento.codigo).zfill(8),  # Codigo IPRESS de la prestadora del servicio (6)
                establecimiento.fuas_categoria,  # Categoria de la IPRESS (Parametro de Configuracion de IPRESS) (7)
                establecimiento.fuas_nivel,  # Nivel (Parametro de Configuracion de IPRESS) (8)
                "",  # Punto digitacion no aplica para el FUA Electronico (9)
                'N',  # Si es reconsideracion (10)
                '',  # Condicional a si es reconsideracion (11)
                '',  # Condicional a si es reconsideracion (12)
                '',  # Condicional a si es reconsideracion (13)
                establecimiento.fuas_codconvenido,  # Codigo convenio (Parametro de Configuracion de IPRESS) (14)
                datos_sis.get("regimen", ""),  # Codigo de componente del asegurado (15)
                datos_sis.get('disa', ""),  # DISA del formato del asegurado SIS (Condicional) (16)
                datos_sis.get('tipo_formato', ""),  # Lote del formato del asegurado SIS (17)
                datos_sis.get("nro_contrato", ""),  # Numero del formato del asegurado SIS (18)
                datos_sis.get("correlativo", ""),
                # Correlativo del integrante del asegurado, y secuencia para las inscripciones # noqa (19)
                datos_sis.get("tabla", ""),
                # Codigo que hace correspondencia a la tabla donde se almacena el contrato del asegurado SIS # noqa (20)
                datos_sis.get("id_numero_registro", ""),
                # dentificador que hace referencia al registro en la tabla del contrato del asegurado SIS # noqa (21)
                datos_sis.get("id_plan", ""),  # Plan de cobertura del asegurado (22)
                datos_sis.get("id_grupo_poblacional", ""),  # Grupo poblacional del asegurado (23)
                datos_sis.get("tipo_documento", ""),
                # Identificador del Tipo de documento de identidad del asegurado (24)
                ciudadano.get("numero_documento", ""),  # Numero del documento de identidad del Asegurado (25)
                u"{}".format(ciudadano.get("apellido_paterno", "")).encode("utf-8"),  # (26)
                u"{}".format(ciudadano.get("apellido_materno", "")).encode("utf-8"),  # (27)
                ciudadano.get("nombres", ""),  # (28)
                "",  # Otros Nombres (29)
                fecha_nacimiento if fecha_nacimiento else '',  # (30)
                datos_sis.get("genero", ""),  # (31)
                datos_sis.get("id_ubigeo", ""),  # Codigo del distrito del asegurado (32)
                # Historia Clinica del asegurado
                HistoriaClinica.objects.get(establecimiento=control.establecimiento, paciente=control.paciente).numero,
                # (33)
                "1",  # Tipo de Atencion  (34)
                "1",  # Condicion Materna del asegurado  (35)
                "1",  # Modalidad de Atencion  (36)
                "",  # Numero de Autorizacion (Condicional a la modalidad de atencion)  (37)
                "",  # Monto Autorizado por el concepto prestacional (Condicional a la modalidad de atencion)  (38)
                "{:%d/%m/%Y %H:%M}".format(control.atencion_fecha),  # Fecha y hora de la Atencion  (39)
                "",  # (40)
                "",  # (41)
                "009",  # Codigo prestacional ( Gestantes )  (42)
                "1",  # Personal que atiende ( Personal del establecimiento )  (43)
                "1",  # Lugar que atiende ( Intramural )  (44)
                "2",  # Destino del afiliado (Con cita )  (45)
                "",  # 46
                "",  # 47
                "",  # 48
                "",  # 49
                "{:%d/%m/%Y}".format(control.fecha_probable_parto),  # 50 Fecha probable de parto
                "",  # 51
                "",  # 52
                "",  # 53
                "",  # 54
                "",  # 55
                "",  # 56
                "",  # 57
                "",  # 58
                "",  # 59
                "",  # 60
                "",  # 61
                "",  # 62
                "",  # 63
                "",  # 64
                "",  # 65
                "",  # 66
                "",  # 67
                "",  # 68
                "",  # 69
                "",  # 70
                "",  # 71
                "1",  # 72
                control.created_by.dni,  # 73
                "04",  # tipo de personal de salud que atiende (74)
                "",  # 75
                "0",  # Estado de egresado 0=Egresado 1= No egresado (76)
                "",  # 77
                "",  # 78
                current_year,  # 79
                current_month,  # 80
                "1",  # 81
                control.created_by.dni,  # 82
                "{:%d/%m/%Y %H:%M}".format(timezone.now()),  # 83
                "",  # 84
                "000000001",  # 85 (Version del aplicativo con el que se registro la prestacion)
            ]
            num_generado = "{}-{}-{}".format(establecimiento.fuas_disa,
                                             timezone.now().strftime('%y'),
                                             str(numerofua).zfill(8))

            return fila, 1, num_generado
        except Exception as ex:
            self.stdout.write("Error en generar la atencion: %s" % control.id)
            self.stderr.write(ex.message)
            return None, 0, ""

    def handle(self, *args, **options):

        if options['establecimiento'] is None:
            raise CommandError('Option `--establecimiento=...` debe especificar un valor para este parametro.')

        if options['date'] is None:
            raise CommandError('Option `--date=...` debe especificar un valor para este parametro.')

        if options['semana'] is None:
            raise CommandError('Option `--semana=...` debe especificar un valor para este parametro.')

        diasemana = datetime.datetime.today().weekday()
        if diasemana == int(options['semana']):

            renaes_est = options['establecimiento']
            sfecha = options['date']

            try:
                fecha = datetime.strptime(sfecha, "%d/%m/%Y")
            except ValueError:
                raise CommandError('Option `--date=...` debe especificar un fecha valida.')

            try:
                establecimiento = Establecimiento.objects.get(codigo=renaes_est)
            except:
                raise CommandError("El establecimiento no existe")

            if not establecimiento.fuas_numinicial or \
                not establecimiento.fuas_numfinal or \
                not establecimiento.fuas_udr or \
                not establecimiento.fuas_categoria or \
                not establecimiento.fuas_nivel or \
                not establecimiento.fuas_disa or \
                not establecimiento.fuas_codconvenido:

                raise CommandError("El establecimiento no cuenta con las "
                                   "configuraciones obligatorias para iniciar "
                                   "el proceso de trama FUA")

            hoy = timezone.now()
            try:
                # Segun la prestacion se toma en cuenta los diagnosticos a tomar en cuenta
                controles = Control.objects.filter(
                    paciente__seguro_sis=True,
                    establecimiento__codigo=renaes_est,
                    establecimiento__fuas_trama=True,
                    atencion_fecha__gte=fecha,
                    atencion_fecha__lte=hoy.date(),
                    diagnostico__detalles__cie__codigo__iexact="z349",
                    numero__lte=13
                ).filter(
                    Q(istramafua=False) | Q(istramafua__isnull=True)
                ).order_by('-atencion_fecha')

                filezip_name = '{}{}.zip'.format(renaes_est.zfill(8), hoy.strftime('%Y%m%d'))

                # Se construye una fila de la tencion segun el documento TRAMA Version 2.0 SIS
                fatencion = open('ATENCION.txt', 'w')
                atencion = csv.writer(fatencion, delimiter='|',
                                      quoting=csv.QUOTE_NONE)

                # Se construye una fila de la atencion segun el documento TRAMA Version 2.0 SIS
                fatenciondiag = open('ATENCIONDIA.txt', 'w')
                atenciondiag = csv.writer(fatenciondiag, delimiter='|',
                                          quoting=csv.QUOTE_NONE)

                num_filas_atencion = 0
                num_filas_diagnostico = 0

                controlesvalidos = []
                for control in controles:
                    control.istramafua = False
                    filaatencion, registro_afectados_atencion, num_generado = self.generar_atencion(control)
                    if registro_afectados_atencion != 0:
                        # implica que se genero correctamente la atencion (Requisito obligatorio de la trama)
                        filadiagnosticos, registros_afectados_diagnostico = self.generar_diagnosticos(control)
                        # implica que se genero correctamente los diagnosticos (Requisito obligatorio de la trama)
                        if registros_afectados_diagnostico != 0:
                            atencion.writerow(filaatencion)
                            atenciondiag.writerows(filadiagnosticos)
                            num_filas_diagnostico += registros_afectados_diagnostico
                            num_filas_atencion += registro_afectados_atencion
                            control.istramafua = True
                            control.numero_fua_asiganado = num_generado
                            establecimiento.fuas_incremento += 1
                            establecimiento.save()

                    control.save()
                    if control.istramafua:
                        controlesvalidos.append(control)
                        self.stdout.write(
                            "Se envio correctamente la atencion al SIS con identificacion de control %s" % control.id)

                    # espera antes de continuar
                    sleep(0.1)

                if num_filas_atencion >= 1:

                    with open('ATENCIONMED.txt', 'w'):
                        pass
                    with open('ATENCIONSMI.txt', 'w'):
                        pass
                    with open('ATENCIONINS.txt', 'w'):
                        pass
                    with open('ATENCIONPRO.txt', 'w'):
                        pass
                    with open('ATENCIONSER.txt', 'w'):
                        pass
                    with open('ATENCIONRN.txt', 'w'):
                        pass

                    fresumen = open('RESUMEN.txt', 'w')
                    fresumen.write('{}\n'.format(hoy.year))  # 1.- Anio (4 digitos)  # noqa
                    fresumen.write('{}\n'.format(hoy.strftime('%m')))  # 2.- Mes (2 digitos, ejemplo "01" es Enero)  # noqa
                    fresumen.write(
                        '{}\n'.format(hoy.strftime('%d')))  # 3.- Numero de Envio (2 digitos, ejemplo:"01" es primer envio
                    fresumen.write('{}\n'.format(filezip_name))  # 4.- Nombre del Paquete (incluyendo la extension .zip)
                    fresumen.write('{}\n'.format("0200"))  # 5.- Version de la Trama (Maximo numero de 10 digitos)1
                    fresumen.write(
                        '{}\n'.format(num_filas_atencion))  # 6.- Numero de Filas con datos del archivo ATENCION.txt  # noqa
                    fresumen.write('{}\n'.format("0"))  # 7.-Numero de Filas con datos del archivo ATENCIONSMI.txt
                    fresumen.write('{}\n'.format(
                        num_filas_diagnostico))  # 8.- Numero de Filas con datos del archivo ATENCIONDIA.txt  # noqa
                    fresumen.write('{}\n'.format("0"))  # 9.- Numero de Filas con datos del archivo ATENCIONMED.txt
                    fresumen.write('{}\n'.format("0"))  # 10.- Numero de Filas con datos del archivo ATENCIONINS.txt
                    fresumen.write('{}\n'.format("0"))  # 11.- Numero de Filas con datos del archivo ATENCIONPROC.txt
                    fresumen.write('{}\n'.format("0"))  # 12.- Numero de Filas con datos del archivo ATENCIONSER.txt
                    fresumen.write('{}\n'.format("0"))  # 13.- Numero de Filas con datos del archivo ATENCIONRN.txt
                    fresumen.write('{}\n'.format("WAWARED"))  # 14.- Nombre del Aplicativo.
                    fresumen.write('{}\n'.format("1.0.0"))  # 15.- Version del Aplicativo.
                    fresumen.write('{}\n'.format("1.0.0"))  # 16.- Version de Envio
                    fresumen.write('{}\n'.format("1"))  # 17.- Tipo de documento del responsable de envio (1=DNI; 3=CE)
                    fresumen.write('{}\n'.format("40734031"))  # 18.- Numero de documento del responsable de envio.

                    fatencion.close()
                    fatenciondiag.close()
                    fresumen.close()
                    subprocess.call(
                        ["zip", "-P", settings.CLAVE_SIS_TRAMA, "-r", filezip_name, "ATENCION.txt",
                         "ATENCIONMED.txt", "ATENCIONSMI.txt", "ATENCIONINS.txt",
                         "ATENCIONPRO.txt", "ATENCIONSER.txt", "ATENCIONRN.txt",
                         "ATENCIONDIA.txt", "RESUMEN.txt"])

                    os.remove('ATENCIONMED.txt')
                    os.remove('ATENCIONSMI.txt')
                    os.remove('ATENCIONINS.txt')
                    os.remove('ATENCIONPRO.txt')
                    os.remove('ATENCIONSER.txt')
                    os.remove('ATENCIONRN.txt')
                    os.remove('RESUMEN.txt')

                    # Envio de la trama FUA
                    data = {
                        'zipfile_name': filezip_name
                    }

                    path = settings.BASE_DIR

                    files = [
                        ('zipfile', open('{}/{}'.format(path, filezip_name), 'rb')),
                    ]

                    try:

                        response = requests.post('{}/api/v1/sis/fua-packages/'.format(settings.EXSER_HOST),
                                                 data=data, files=files, headers={
                                'X-Api-Token': '{}'.format(settings.EXSER_TOKEN)
                            })

                        data = response.json()
                        for control in controlesvalidos:
                            control.fua_identificador_envio_trama = data["id"]  # Id de transaccion
                            control.save()

                        self.stdout.write('Las atenciones fueron procesadas y enviadas al SIS satisfactoriamente')

                    except Exception as ex:
                        raise CommandError("Error {} al enviar el paquete zip FUA {} al SIS".format(ex.message, filezip_name))

                else:
                    self.stdout.write('no existe FUA a generar')
                    fatencion.close()
                    fatenciondiag.close()

                os.remove('ATENCION.txt')
                os.remove('ATENCIONDIA.txt')

            except Exception as ex:
                raise CommandError("Error al procesar el FUA {}".format(ex.message))
