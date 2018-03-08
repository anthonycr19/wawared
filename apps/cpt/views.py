from django.db.models import Q
from django.http.response import JsonResponse

from .models import CatalogoProcedimiento


def cpt_search(request):
    q = request.GET.get('q', '')
    data = []
    if q:
        for cpt in CatalogoProcedimiento.objects.filter(
                Q(codigo_cpt__icontains=q) | Q(denominacion_procedimientos__icontains=q)):
            data.append({
                'id': cpt.id,
                'codigo': cpt.codigo_cpt,
                'nombre': cpt.denominacion_procedimientos
            })
    return JsonResponse(data, safe=False)
