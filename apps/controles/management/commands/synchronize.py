import datetime
from time import sleep
import requests
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from controles.models import Control, Diagnostico
from citas.models import Cita
from django.conf import settings
from embarazos.models import UltimoEmbarazo


class Command(BaseCommand):
    help = 'Sincronizar los registros de wawared con los de la maternidad de lima'
    option_list = BaseCommand.option_list + (
        make_option(
            "-e",
            "--establecimiento",
            dest="establecimiento",
            help="Indica el establecimiento para el cual se esta corriendo la sincronizacion",
            metavar="SLUG"
        ),
    )

    def enviar_control(self, control):
        try:

            cita = control.citas.all()[0] if control.citas.all().count() != 0 else None
            if cita and not cita.codigo_origen_externo is None:

                procedimientos = Diagnostico.objects.filter(control_id=control.id)[0].procedimientos.all().count()
                diagnostico = Diagnostico.objects.filter(control_id=control.id)[0].detalles.all().count()
                nro_controles = Control.objects.filter(paciente=control.paciente, embarazo=control.embarazo,
                                                       citas__tipo=Cita.TIPO_CONTROL).exclude(id=control.id).count()

                if procedimientos != 0:
                    jsonlistproc = list(
                        Diagnostico.objects.filter(control_id=control.id)[0].procedimientos.all().values(
                            'cpt__codigo_cpt'))  # json.dumps(, cls=DjangoJSONEncoder)
                else:
                    jsonlistproc = ""

                if diagnostico != 0:
                    jsonlistdiag = list(
                        Diagnostico.objects.filter(control_id=control.id)[0].detalles.all().values('cie__codigo',
                                                                                                   'tipo'))  # json.dumps(,cls=DjangoJSONEncoder)
                else:
                    jsonlistdiag = ""

                datajson = {
                    "codigo_externo": cita.codigo_origen_externo,
                    "nro_gestas": UltimoEmbarazo.objects.filter(paciente=control.paciente).count(),
                    "tiempo_gestas": control.edad_gestacional_semanas,
                    "tipo_consulta": "NU" if nro_controles == 0 else "CO",
                    "codigo_renaes": control.establecimiento.codigo,
                    "nro_controles": nro_controles,
                    "tipo_atencion": "A",
                    "tipo_paciente": "E",
                    "riesgo_obstetrico": "B",
                    "nro_interconsulta": 0,
                    "totalHoras": 4 if control.citas.all()[0].tipo != 'control' else 0,
                    "diagnosticos": jsonlistdiag,
                    "procedimientos": jsonlistproc
                }

                r = requests.post("%s%s" % (settings.API_SYNCHRONIZE_MIRTH, 'Atencion/registrar/'), json=datajson)

                respuesta = r.json()
                if respuesta['status'] == 'OK':
                    return True
                else:
                    self.stdout.write("Error : %s" % respuesta['descripcion'])
                    return None
            else:
                return True
        except Exception as e:
            self.stdout.write("Error : %s" % e.message)
            return None

    def handle(self, *args, **options):

        if options['establecimiento'] == None:
            raise CommandError("Option `--establecimiento=...` debe especificar un valor para este parametro.")

        id_est = options['establecimiento']

        controles = Control.objects.filter(synchronize=None, establecimiento_id=id_est)

        for control in controles:

            control.synchronize = self.enviar_control(control)
            control.save()
            if control.synchronize:
                self.stdout.write("Se sincronizo correctamente el control %s" % control.id)

            # espera antes de continuar
            sleep(0.1)
