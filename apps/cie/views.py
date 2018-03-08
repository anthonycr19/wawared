from django.db.models import Q
from django.http.response import JsonResponse

from .models import ICD10


def cie_search(request):
    q = request.GET.get('q', '')
    data = []
    if q:
        for cie in ICD10.objects.filter(
                Q(codigo__icontains=q) | Q(nombre__icontains=q)):
            if cie.nombre_mostrar:
                tmp_nombre_mostrar = cie.nombre_mostrar.title()
            else:
                tmp_nombre_mostrar = cie.nombre.title()
            data.append({
                'id': cie.id,
                'codigo': cie.codigo,
                'nombre': tmp_nombre_mostrar
            })
    return JsonResponse(data, safe=False)
