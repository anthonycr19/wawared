import importlib

from cita_client.client import CITAClient
from django.conf import settings
from mpi_client.client import MPIClient


class CiudadanoRest(object):
    url = settings.MPI_API_URL
    url_citas_minsa = settings.CITA_API_URL
    EC_CHOICES = {"1": "soltera", "4": "divorciada", "2": "casada", "5": "viuda", "3": "conviviente"}
    OC_CHOICES = {"01": "1", "02": "2", "03": "3", "04": "4", "05": "5", "06": "6", "07": "7", "08": "8"}
    GI_CHOICES = {"00": "11", "01": "-1", "02": "12", "03": "12", "04": "-1", "05": "13", "06": "13", "07": "15",
                  "08": "15", "09": "14", "10": "14", "11": "-1", "12": "-1"}
    TD_CHOICES = {"00": "noespecifica", "01": "dni", "02": "lm", "03": "ce", "04": "partidanacimiento",
                  "06": "pasaporte", "07": "nie"}

    def get_persona_por_dni(self, dni, solo_mujer=True):
        mpi_client_var = MPIClient(settings.MPI_API_TOKEN)
        response = mpi_client_var.get('{0}/api/v1/ciudadano/ver/01/{1}/'.format(self.url, dni))
        return self.get_paciente(response, solo_mujer)

    def get_persona_por_uuid(self, uuid):
        cita_client_var = CITAClient()
        url_citas = '{0}api/paciente/buscaruuid/{1}/'.format(self.url_citas_minsa, uuid)
        response = cita_client_var.get(url_citas)
        return self.get_paciente(response, False)

    def get_persona_por_tipo_documento(self, tipo_documento, numero_documento, codigo_renaes):
        cita_client_var = CITAClient()
        url_citas = '{0}api/paciente/ver/{1}/{2}/{3}/'.format(self.url_citas_minsa, tipo_documento,
                                                              numero_documento, codigo_renaes)
        response = cita_client_var.get(url_citas)
        return self.get_paciente(response, False)

    def get_paciente(self, response_data, solo_mujer):
        try:
            json_persona = response_data.json()
            json_attributes = json_persona['data']['attributes']
            module_pacientes = importlib.import_module('pacientes.models')
            module_ubigeo = importlib.import_module('ubigeo.models')
            paciente_class = getattr(module_pacientes, 'Paciente')

            if solo_mujer:
                if json_attributes.get('sexo') == '1':
                    return "Este DNI es de un sexo masculino"
            paciente = paciente_class()
            paciente.nombres = json_attributes.get('nombres')
            paciente.apellido_paterno = json_attributes.get('apellido_paterno')
            paciente.apellido_materno = json_attributes.get('apellido_materno')
            paciente.tipo_documento = self.TD_CHOICES[json_attributes.get('tipo_documento')]  # 'dni'
            paciente.fecha_nacimiento = json_attributes.get('fecha_nacimiento')

            if json_attributes.get('domicilio_direccion') is None:
                paciente.direccion = ''
            else:
                paciente.direccion = json_attributes.get('domicilio_direccion')
            paciente.numero_documento = json_attributes.get('numero_documento')
            pais_class = getattr(module_ubigeo, 'Pais')
            pais = pais_class.objects.get(codigo='PE')
            paciente.pais_nacimiento = pais
            ocupacion_class = getattr(module_pacientes, 'Ocupacion')

            if json_attributes.get('ocupacion') is None:
                ocupacion = ocupacion_class.objects.get(id=8)
            else:
                ocupacion = ocupacion_class.objects.get(id=self.OC_CHOICES[json_attributes.get('ocupacion')])
            paciente.ocupacion = ocupacion
            paciente.estado_civil = self.EC_CHOICES[json_attributes.get('estado_civil')]
            paciente.email = json_attributes.get('correo')
            paciente.pais_residencia = pais
            departamento_residencia_id = '{}0000'.format(json_attributes.get('get_departamento_domicilio_ubigeo_inei'))
            provincia_residencia_id = '{}00'.format(json_attributes.get('get_provincia_domicilio_ubigeo_inei'))
            distrito_residencia_id = json_attributes.get('get_distrito_domicilio_ubigeo_inei')
            obj_departamento_residencia = self.get_ubigeo(module_ubigeo, departamento_residencia_id, 'DEPARTAMENTO')
            obj_provincia_residencia = self.get_ubigeo(module_ubigeo, provincia_residencia_id, 'PROVINCIA')
            obj_distrito_residencia = self.get_ubigeo(module_ubigeo, distrito_residencia_id, 'DISTRITO')

            if obj_departamento_residencia:
                paciente.departamento_residencia = obj_departamento_residencia
            if obj_provincia_residencia:
                paciente.provincia_residencia = obj_provincia_residencia
            if obj_distrito_residencia:
                paciente.distrito_residencia = obj_distrito_residencia
            if not json_attributes.get('nacimiento_ubigeo') is None:
                ubigeo_nac_id = json_attributes.get('nacimiento_ubigeo').rjust(6, "0")
                departamento_nac_id = ubigeo_nac_id[:-4].ljust(6, "0")
                provincia_nac_id = ubigeo_nac_id[:-2].ljust(6, "0")
                paciente.departamento_nacimiento = self.get_ubigeo(module_ubigeo, departamento_nac_id, 'DEPARTAMENTO')
                paciente.provincia_nacimiento = self.get_ubigeo(module_ubigeo, provincia_nac_id, 'PROVINCIA')
            if not json_attributes.get('etnia') is None:
                etnia_val = self.get_etnia(module_pacientes, json_attributes.get('etnia'))

                if etnia_val:
                    paciente.etnia = etnia_val
                else:
                    etnia_class = getattr(module_pacientes, 'Etnia')
                    etnia_default = etnia_class.objects.get(id=73)
                    paciente.etnia = etnia_default
            else:
                etnia_class = getattr(module_pacientes, 'Etnia')
                etnia_default = etnia_class.objects.get(id=73)
                paciente.etnia = etnia_default

            if not json_attributes.get('grado_instruccion') is None:
                estudio_id = self.GI_CHOICES[json_attributes.get('grado_instruccion')]
                if estudio_id == '-1':
                    paciente.estudio = None
                else:
                    estudio_class = getattr(module_pacientes, 'Estudio')
                    estudio = estudio_class.objects.get(id=estudio_id)
                    paciente.estudio = estudio
            if not json_attributes.get('tipo_seguro') is None:
                seguro_id = json_attributes.get('tipo_seguro')

                if seguro_id in ('2'):
                    paciente.seguro_sis = True
                else:
                    if seguro_id in ('3'):
                        paciente.seguro_essalud = True
                    else:
                        if seguro_id in ('9'):
                            paciente.seguro_privado = True
                        else:
                            if seguro_id in ('5', '6', '7', '8'):
                                paciente.seguro_sanidad = True
                            else:
                                paciente.seguro_otros = True
            paciente.origen_phr = True
            return paciente
        except Exception as e:
            print(e)
            return None

    def get_etnia(self, module_pacientes, codigo_etnia):
        try:
            etnia_class = getattr(module_pacientes, 'Etnia')
            etnia = etnia_class.objects.get(codigo=codigo_etnia)
            return etnia
        except Exception as e:
            return None

    def get_ubigeo(self, module_ubigeo, codigo_ubigeo, tipo):
        try:
            departamento_class = getattr(module_ubigeo, 'Departamento')
            provincia_class = getattr(module_ubigeo, 'Provincia')
            distrito_class = getattr(module_ubigeo, 'Distrito')

            if tipo in ('DEPARTAMENTO'):
                ubigeo = departamento_class.objects.get(codigo=codigo_ubigeo)
                return ubigeo
            if tipo in ('PROVINCIA'):
                ubigeo = provincia_class.objects.get(codigo=codigo_ubigeo)
                return ubigeo
            if tipo in ('DISTRITO'):
                ubigeo = distrito_class.objects.get(codigo=codigo_ubigeo)
                return ubigeo
            return None
        except Exception as e:
            return None
