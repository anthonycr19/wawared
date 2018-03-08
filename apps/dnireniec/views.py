from django.http.response import JsonResponse
import suds
from suds.sax.element import Element
from models import ServicioReniec


def json_response(num_dni):
    objServicio = ServicioReniec.objects.get(id=1)

    ns = objServicio.namespace  # 'http://tempuri.org/'
    url = objServicio.urlwsdlservice  # 'http://ws_min.minsa.gob.pe/wsreniecmq/serviciomq.asmx?wsdl'
    app = objServicio.appservice  # 'WAWARED'
    usuario = objServicio.userservice  # '05353734'
    clave = objServicio.passservice  # '/*_waw@r3d+$'

    tem_ns = ('tem', ns)
    cliente = suds.client.Client(url)

    h_app = Element('app', ns=tem_ns)
    h_usuario = Element('usuario', ns=tem_ns)
    h_clave = Element('clave', ns=tem_ns)

    h_app.setText(app)
    h_usuario.setText(usuario)
    h_clave.setText(clave)

    h_credentialmq = Element('Credencialmq', ns=tem_ns)
    h_credentialmq.insert(h_app)
    h_credentialmq.insert(h_usuario)
    h_credentialmq.insert(h_clave)

    cliente.set_options(soapheaders=h_credentialmq)
    resultado = cliente.service.obtenerDatosCompletos(num_dni)

    return JsonResponse(resultado[0], safe=False)


def consultadni(request, num_dni):
    return json_response(num_dni)
