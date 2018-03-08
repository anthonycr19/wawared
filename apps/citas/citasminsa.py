from django.conf import settings
import requests
import importlib
import json
from datetime import datetime
import os

from citas.models import Cita
from pacientes.models import Paciente, HistoriaClinica
from pacientes.ciudadano import CiudadanoRest
from cita_client.client import CITAClient


class CitasRest(object):
    url = settings.CITA_API_URL

    def get_citas(self, establecimiento, usuario, fecha):
        try:
            cita_client_var = CITAClient()

            # '01'--> tipo dni para el sistemas de citas
            payload = {'tipo_doc': '01', 'num_doc': usuario.dni, 'fecha': fecha}

            url_citas = '{0}api/citas/establecimiento/{1}/aplicacion/{2}/'.format(self.url, establecimiento.codigo,
                                                                                  settings.APP_IDENTIFIER)

            response = cita_client_var.get(url_citas, params=payload)  # requests.get(url_citas, params = payload)

            json_citas = response.json()
            cantidad_citas = json_citas['meta']['pagination']['count']
            lista_citas = []

            if cantidad_citas > 0:
                resultados_json = json_citas['results']

                for cita_json in resultados_json:
                    uuid_cita_minsa = cita_json.get('uuid_cita')
                    cita = self.get_cita_x_uuid(uuid_cita_minsa)

                    if cita:
                        if not cita.asistio:
                            lista_citas.append(cita)
                    else:
                        pac_numero_documento = cita_json.get('paciente').get('numero_documento')
                        pac_tipo_documento = cita_json.get('paciente').get('tipo_documento', 'dni')

                        if pac_tipo_documento == '01':
                            pac_tipo_documento = 'dni'

                        paciente = self.get_paciente_x_documento(pac_tipo_documento, pac_numero_documento)

                        if not paciente:
                            # consultar api de admision
                            uuid_paciente = cita_json.get('paciente').get('id_phr')
                            ciudadano_rest = CiudadanoRest()
                            paciente = ciudadano_rest.get_persona_por_uuid(uuid_paciente)

                            if paciente:
                                paciente.save()
                                HistoriaClinica.objects.create(
                                    numero=paciente.numero_documento,
                                    establecimiento_id=establecimiento.id,
                                    paciente=paciente
                                )

                        if paciente:
                            cita = Cita()
                            cita.origen = 'externo'
                            cita.paciente = paciente
                            cita.establecimiento = establecimiento
                            cita.tipo = 'control'  # por verificar
                            cita.fecha = datetime.strptime('{} {}'.format(cita_json.get('fecha_cita'), \
                                                                          cita_json.get('hora_inicio')),
                                                           '%Y-%m-%d %H:%M:%S')
                            cita.fecha_asistio = None
                            cita.is_wawared = False
                            cita.asistio = False
                            cita.especialista = usuario
                            cita.uuid_cita_minsa = uuid_cita_minsa
                            cita.save()

                            lista_citas.append(cita)

            return lista_citas

        except Exception as e:
            return None

    def confirmar_cita(self, uuid_cita_minsa, tiempo_atencion):
        try:
            cita_client_var = CITAClient()
            payload = {'uuid_cita': uuid_cita_minsa, 'duracion': tiempo_atencion, 'estado': 3}
            response = cita_client_var.post('{0}api/citas/AtencionNew/'.format(self.url), json=payload)
        except Exception as e:
            print(e)
            return None

    def get_cita_x_uuid(self, uuid_cita_minsa):
        try:
            cita = Cita.objects.get(uuid_cita_minsa=uuid_cita_minsa)
            return cita
        except Cita.objects.DoesNotExist as e:
            return None

    def get_paciente_x_documento(self, tipo_documento, numero_documento):
        paciente = Paciente.objects.filter(tipo_documento=tipo_documento,
                                           numero_documento=numero_documento).first()

        return paciente
