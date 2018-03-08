import logging

from datetime import datetime
import json
from django.db import IntegrityError

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from citas.models import Cita
from pacientes.models import Paciente, HistoriaClinica
from ubigeo.models import Pais, Departamento, Provincia, Distrito
from establecimientos.models import Establecimiento
from perfiles.models import User
from pacientes.ciudadano import CiudadanoRest
from partos.models import Ingreso

logger = logging.getLogger(__name__)

class PacienteException(Exception):
    pass


class PacienteDNIView(View):
    def get(self, request, *args, **kwargs):
        try:
            paciente = Paciente.objects.get(
                tipo_documento=Paciente.DOCUMENTO_DNI,
                numero_documento=kwargs.get('dni', 0))

            if paciente.estado_civil:
                tmp_estado_civil = paciente.estado_civil.upper()
            else:
                tmp_estado_civil = ''

            data = {
                'nombres': paciente.nombres,
                'apellido_paterno': paciente.apellido_paterno,
                'apellido_materno': paciente.apellido_materno,
                'fecha_nacimiento': paciente.fecha_nacimiento.strftime(
                    '%d/%m/%Y'),
                'direccion': paciente.direccion,
                'urbanizacion': paciente.urbanizacion,
                'estudios': paciente.estudio_nombre,
                'estado_civil': tmp_estado_civil,
                'seguro_sis': paciente.seguro_sis,
                'seguro_essalud': paciente.seguro_essalud,
                'seguro_privado': paciente.seguro_privado,
                'seguro_sanidad': paciente.seguro_sanidad,
                'seguro_otros': paciente.seguro_otros,
                'codigo_afiliacion': paciente.codigo_afiliacion
            }
            return JsonResponse(data)
        except Paciente.DoesNotExist:
            return JsonResponse({
                'message': 'DNI invalido'
            }, status=404)


class PacienteCiudadanoView(View):
    def get(self, request, *args, **kwargs):
        try:

            if kwargs.get('tipodoc'):
                paciente = Paciente.objects.filter(
                    tipo_documento=kwargs.get('tipodoc'),
                    numero_documento=kwargs.get('nrodoc')
                ).first()
            else:
                paciente = CiudadanoRest().get_persona_por_dni(kwargs.get('dni'), False)

            if not paciente is None:

                departamento_nacimiento = ""
                provincia_nacimiento = ""
                departamento_residencia = ""
                provincia_residencia = ""
                distrito_residencia = ""
                estudio = ""
                etnia = ""
                estado_civil = ""
                ocupacion = ""

                if not paciente.departamento_nacimiento is None:
                    departamento_nacimiento = paciente.departamento_nacimiento.nombre

                if not paciente.provincia_nacimiento is None:
                    provincia_nacimiento = paciente.provincia_nacimiento.nombre

                if not paciente.departamento_residencia is None:
                    departamento_residencia = paciente.departamento_residencia.nombre

                if not paciente.provincia_residencia is None:
                    provincia_residencia = paciente.provincia_residencia.nombre

                if not paciente.distrito_residencia is None:
                    distrito_residencia = paciente.distrito_residencia.nombre

                fecha_nacimiento = '{}'.format(paciente.fecha_nacimiento)

                if not paciente.estudio is None:
                    estudio = paciente.estudio.nombre

                if not paciente.etnia is None:
                    etnia = paciente.etnia.nombre

                if not paciente.estado_civil is None:
                    estado_civil = paciente.estado_civil

                if not paciente.ocupacion is None:
                    ocupacion = paciente.ocupacion.nombre

                embarazosprevios = []

                embarazo = paciente.get_embarazo_actual()

                try:
                    ant = paciente.antecedente_obstetrico.__dict__
                    resumenantecedente = {name: ant[name] for name in ant if not name.startswith('_')}
                except Exception as e:
                    logger.warning('Error al conectar con MPI', exc_info=True)
                    resumenantecedente = {}

                if embarazo is not None:
                    ultimosembarazos = paciente.ultimos_embarazos.all().exclude(embarazo=embarazo).order_by('numero')
                else:
                    ultimosembarazos = paciente.ultimos_embarazos.all().order_by('numero')

                for cembarazo in ultimosembarazos:
                    cemb = {
                        'gestacion': cembarazo.numero,
                        'tipo': cembarazo.tipo,
                        'tipo_display': cembarazo.get_tipo_display(),
                        'numfetos': 0,
                        'fetos': []
                    }
                    for bebe in cembarazo.bebes.all():
                        cemb['fetos'].append(
                            {
                                'fecha': bebe.fecha.strftime('%d/%m/%Y'),
                                'terminacion': bebe.terminacion,
                                'terminacion_display': bebe.get_terminacion_display(),
                                'aborto': bebe.aborto,
                                'aborto_display': bebe.get_aborto_display(),
                                'vive': bebe.vive,
                                'muerte': bebe.muerte,
                                'muerte_display': bebe.get_muerte_display(),
                                'peso': bebe.peso,
                                'sexo': bebe.sexo,
                                'sexo_display': bebe.get_sexo_display(),
                                'edad_gestacional': bebe.edad_gestacional,
                                'lugar': bebe.lugar,
                                'lugar_display': bebe.get_lugar_display(),
                                'lactancia': bebe.lactancia,
                                'lactancia_display': bebe.get_lactancia_display()
                            }
                        )
                        cemb['numfetos'] += 1

                    embarazosprevios.append(cemb)

                detalle = {}
                if embarazo is not None:
                    ingreso = Ingreso.objects.filter(embarazo=embarazo).first()
                    if ingreso is None:
                        ultimocontrol = embarazo.controles.last()
                        detalle['gestante'] = {
                            'altura_uterina': ultimocontrol.altura_uterina,
                            'edad_gestacional': ultimocontrol.edad_gestacional_semanas,
                            'fur': embarazo.fum.strftime(
                                '%d/%m/%Y')
                        }
                else:
                    embarazo = paciente.ultimos_embarazos.all().last()
                    ingreso = Ingreso.objects.filter(embarazo=embarazo).first()
                    if ingreso is not None:
                        ultimoembarazo = paciente.ultimos_embarazos.filter(embarazo=embarazo)
                        if ultimoembarazo:
                            fetos = []
                            for cembarazo in ultimoembarazo:
                                for bebe in cembarazo.bebes.all():
                                    fetos.append(
                                        {
                                            'fecha': bebe.fecha.strftime('%d/%m/%Y'),
                                            'terminacion': bebe.terminacion,
                                            'terminacion_display': bebe.get_terminacion_display(),
                                            'aborto': bebe.aborto,
                                            'aborto_display': bebe.get_aborto_display(),
                                            'vive': bebe.vive,
                                            'muerte': bebe.muerte,
                                            'muerte_display': bebe.get_muerte_display(),
                                            'peso': bebe.peso,
                                            'sexo': bebe.sexo,
                                            'sexo_display': bebe.get_sexo_display(),
                                            'lugar': bebe.lugar,
                                            'lugar_display': bebe.get_lugar_display(),
                                        }
                                    )
                            detalle['parto'] = {
                                'edad_gestacional': ingreso.edad_gestacional_semanas,
                                'num_gestacion': ultimoembarazo[0].numero,
                                'tipo_gestacion': ultimoembarazo[0].get_tipo_display(),
                                'num_fetos': len(fetos),
                                'fetos': fetos
                            }

                datos = {
                    'NOMBRE': paciente.nombres,
                    'PATERNO': paciente.apellido_paterno,
                    'MATERNO': paciente.apellido_materno,
                    'FECHA_NACIMIENTO': '{0}/{1}/{2}'.format(fecha_nacimiento[8:10], fecha_nacimiento[5:7],
                                                             fecha_nacimiento[0:4]),
                    'DEPART_NACIMIENTO': departamento_nacimiento,
                    'PROV_NACIMIENTO': provincia_nacimiento,
                    'DEPART_RESIDENCIA': departamento_residencia,
                    'PROV_RESIDENCIA': provincia_residencia,
                    'DIST_RESIDENCIA': distrito_residencia,
                    'DIRECCION_RESIDENCIA': paciente.direccion,
                    'ESTUDIO': estudio,
                    'ETNIA': etnia,
                    'ESTADO_CIVIL': estado_civil,
                    'OCUPACION': ocupacion,
                    'condicion': detalle,
                    'antecedentes': {
                        'detalle': embarazosprevios,
                        'resumen': resumenantecedente
                    }
                }
                return JsonResponse(datos)
            else:
                return JsonResponse({
                    'message': 'Paciente no encontrado'
                }, status=404)


        except Exception as e:
            return JsonResponse({
                'message': 'Error al buscar DNI'
            }, status=500)


class PacienteView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(PacienteView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        response_message = 'Paciente y cita registrados'
        try:

            _data, complete_fields = self.parse_data()

            if not _data:
                raise PacienteException('formato json incorrecto')

            if not complete_fields:
                raise PacienteException('Campos requeridos incompletos')

            try:

                paciente = Paciente.objects.get(
                    tipo_documento=_data['tipo_documento'],
                    numero_documento=_data['numero_documento'])

            except Paciente.DoesNotExist:

                pais_residencia = Pais.objects.get(
                    codigo__iexact=_data['pais_residencia'])

                paciente_data = {
                    'nombres': _data['nombres'],
                    'apellido_paterno': _data['apellido_paterno'],
                    'apellido_materno': _data['apellido_materno'],
                    'numero_documento': _data['numero_documento'],
                    'fecha_nacimiento': datetime.strptime(_data['fecha_nacimiento'], '%d/%m/%Y'),
                    'pais_nacimiento': Pais.objects.get(codigo__iexact=_data['pais_nacimiento']),
                    'pais_residencia': pais_residencia,
                    'direccion': _data['direccion'],
                    'estado_civil': _data['estado_civil'],
                    'seguro_sis': _data['seguro_sis'],
                    'seguro_essalud': _data['seguro_essalud'],
                    'seguro_privado': _data['seguro_privado'],
                    'seguro_sanidad': _data['seguro_sanidad'],
                    'seguro_otros': _data['seguro_otros'],
                    'codigo_afiliacion': _data['codigo_afiliacion'],
                }

                tmp = _data['ubigeo_residencia']

                dep = '{:0<6}'.format(tmp[:2])
                prov = '{:0<6}'.format(tmp[:4])
                dis = tmp

                departamento = Departamento.objects.get(
                    pais=pais_residencia, codigo=dep)
                provincia = Provincia.objects.get(
                    departamento=departamento, codigo=prov)
                distrito = Distrito.objects.get(provincia=provincia, codigo=dis)

                paciente_data.update({
                    'departamento_residencia': departamento,
                    'provincia_residencia': provincia,
                    'distrito_residencia': distrito
                })
                paciente_data['tipo_documento'] = _data['tipo_documento']
                paciente = Paciente(**paciente_data)
                paciente.save()

            if 'cita' in _data:
                cita = self.register_cita(paciente, _data['cita'], _data['hc'])
                if not cita:
                    raise PacienteException(
                        u'Paciente registrado, fecha y hora de cita '
                        'no disponibles')

        except PacienteException as ex:
            response_message = ex.message
            return JsonResponse({'error': response_message}, status=500)
        except (
            Pais.DoesNotExist, Departamento.DoesNotExist,
            Provincia.DoesNotExist, Distrito.DoesNotExist):
            response_message = 'Error en ubigeo'
            return JsonResponse({'error': response_message}, status=500)
        except ValueError as ex:
            response_message = ex.message
            return JsonResponse({'error': response_message}, status=500)
        except Exception as ex:
            response_message = ex.message
            return JsonResponse({'error': response_message}, status=500)

        return JsonResponse({'status': response_message})

    def parse_data(self):

        required_fields = [
            'hc', 'tipo_documento', 'numero_documento', 'nombres',
            'apellido_paterno', 'apellido_materno', 'pais_residencia',
            'ubigeo_residencia', 'fecha_nacimiento', 'pais_nacimiento']
        try:
            _data = {}
            paciente = json.loads(self.request.body)
            flag_required = True
            keys = []
            for field in paciente:
                if isinstance(paciente[field], dict):
                    _data[field] = {}
                    children = paciente[field]
                    for child in children:
                        _data[field][child] = children[child]
                else:
                    _data[field] = paciente[field]
                keys.append(field)

            for required_field in required_fields:
                flag_required = flag_required and required_field in keys

            if not flag_required:
                return _data, False
            else:

                return _data, required_fields
        except:
            return {}, False

    def register_cita(self, paciente, data, hc):

        try:

            fecha = datetime.strptime(data['fecha'], '%d/%m/%Y').date()
            hora = datetime.strptime(data['hora'], '%H:%M').time()
            fecha_hora = datetime.combine(fecha, hora)
            establecimiento = Establecimiento.objects.get(codigo=data['codrenaes'])
            especialista = User.objects.get(dni=data['dni_especialista'])
            cod_cita_externo = data['cod_cita_externo']

            if not HistoriaClinica.objects.filter(establecimiento_id=establecimiento.id, paciente=paciente).exists():
                HistoriaClinica.objects.create(
                    numero=hc,
                    establecimiento_id=establecimiento.id,
                    paciente=paciente
                )

            if not Cita.exists_cita_in_same_date_for_medical_specialist(establecimiento.id, fecha_hora, especialista):
                cita = Cita(
                    paciente=paciente,
                    tipo=Cita.TIPO_GESTACION if data['tipo_cita'] == "gestante" else Cita.TIPO_CONTROL,
                    origen=Cita.ORIGEN_EXTERNO,
                    fecha=fecha_hora,
                    establecimiento_id=establecimiento.id,
                    especialista_id=especialista.id,
                    codigo_origen_externo=cod_cita_externo,
                    is_wawared=False, asistio=False)
                cita.save()
                return cita
            else:
                return None
        except IntegrityError:
            return None
        except Establecimiento.DoesNotExist:
            return None
        except User.DoesNotExist:
            return None
