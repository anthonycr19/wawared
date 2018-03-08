import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
import requests

from ...models import Embarazo
from mensajes.models import Mensajes


class Command(BaseCommand):
    help = 'Send sms messages to women'

    def enviar_sms(self, msg, cel):
        try:
            requests.post('{}/api/v1/messages/'.format(settings.EXSER_HOST), {
                'recipient': '51{}'.format(cel),
                'sender': 'wawared',
                'body': msg,
            }, headers={
                'X-Api-Token': settings.EXSER_TOKEN,
            })
        except Exception as ex:
            self.stderr.write(ex.message)

    def handle(self, *args, **options):
        day = datetime.datetime.today().weekday()

        pregnancies = Embarazo.objects.filter(activo=True, paciente__recibir_sms=True)

        for p in pregnancies:

            week = p.semana_actual_probable()

            if week is None:
                continue

            if week < 1 or week > 41:
                continue

            cel = p.paciente.wawacel()

            if cel is None:
                continue

            try:
                semana = week
                control = p.controles.all().last()
                if control is None:
                    continue
                msg = Mensajes.objects.filter(tipo_mensaje='gestante', semana_mensaje=semana, dia_semana=day).last()
                if msg:
                    cadena = unicode(p.paciente.nombre_completo)
                    nombre = cadena[:8] if len(cadena) > 8 else cadena
                    msg = "%s, %s" % (nombre, msg)
                    if control.proxima_cita:
                        msg = msg.replace("xxxx", control.proxima_cita.strftime("%d/%m"))
                else:
                    continue
            except IndexError:
                continue

            self.enviar_sms(msg, cel)
