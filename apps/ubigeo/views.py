# coding:utf-8
from django.http.response import JsonResponse

from ubigeo.models import Departamento, Distrito, Provincia


def json_response(items):
    result = []
    for i in range(len(items)):
        if i > 0 or items[i].nombre.lower() == 'lima':
            result.append({
                'id': items[i].id,
                'nombre': items[i].nombre,
            })

    return JsonResponse(result, safe=False)


def departamentos(request, id):
    return json_response(Departamento.objects.filter(pais__id=id))


def provincias(request, id):
    return json_response(Provincia.objects.filter(departamento__id=id))


def distritos(request, id):
    return json_response(Distrito.objects.filter(provincia__id=id))
