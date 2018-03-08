# coding:utf-8
from datetime import datetime
import os
import json
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q

from django.shortcuts import get_object_or_404

from common.views import ExcelView
from dashboard.views import EstablecimientoRequiredMixin
from django.views.generic import View
from .models import Establecimiento, DownloadReport
from .reports import (
    SIENReport, GlobalReport, LibroRegistroDiarioSeguimientoGestantesReport, GlobalReportParto, GlobalReportPuerperio)
from . import tasks

DATE_FORMAT = '%d/%m/%Y'


def establecimiento_search(request):
    q = request.GET.get('q', '')
    data = []
    if q:
        for establecimiento in Establecimiento.objects.filter(
                Q(codigo__icontains=q) | Q(nombre__icontains=q)):
            if establecimiento.nombre:
                tmp_nombre_mostrar = establecimiento.nombre.title()
            data.append({
                'id': establecimiento.id,
                'codigo': establecimiento.codigo,
                'nombre': tmp_nombre_mostrar
            })
    return JsonResponse(data, safe=False)


class DownloadReportFileView(EstablecimientoRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        report = get_object_or_404(DownloadReport, id=kwargs.get('report_id'))
        if report.creator != request.user:
            raise PermissionDenied
        if not report.file.name or report.status != 'done':
            messages.warning(
                request,
                'El reporte aun no esta listo, '
                '<a href="{}">Descargar reporte</a>'.format(
                    reverse(
                        'establecimientos:reports:download_report',
                        kwargs={'report_id': report.id})))
            return HttpResponseRedirect('/')
        report_file = open(os.path.join(settings.MEDIA_ROOT, report.file.name))
        response = HttpResponse(
            report_file.read(), content_type=report.content_type)
        report_file.close()
        response['Content-Disposition'] = 'attachment; filename={}'.format(
            report.filename)
        return response


class SIENReportView(EstablecimientoRequiredMixin, ExcelView):
    filename = 'informe_diario_nutricional(SIEN).xlsx'
    establecimiento = None

    def dispatch(self, request, *args, **kwargs):
        self.establecimiento = get_object_or_404(
            Establecimiento, id=request.session['establecimiento_id'])
        return super(SIENReportView, self).dispatch(request, *args, **kwargs)

    def get_book(self, output):
        period = self.request.GET.get('period', 'daily')
        filter_date_str = self.request.GET.get('date', None)
        if filter_date_str:
            filter_date = datetime.strptime(filter_date_str, '%d/%m/%Y')
        else:
            filter_date = datetime.today()
        report = SIENReport(
            self.establecimiento, filter_date=filter_date, period=period)
        return report.get_book(output)


class GlobalReportView(EstablecimientoRequiredMixin, ExcelView):
    filename = 'informe-de-{}-a-{}.xlsx'
    establecimiento_ids = []
    start_date = None
    end_date = None

    def dispatch(self, request, *args, **kwargs):
        self.start_date = datetime.strptime(
            request.GET.get('start_date', ''), DATE_FORMAT)
        self.end_date = datetime.strptime(
            request.GET.get('end_date', ''), DATE_FORMAT)
        self.establecimiento_ids = request.GET.getlist(
            'establecimientos', [request.session['establecimiento_id']])
        if len(self.establecimiento_ids) > 1 and \
            not request.user.has_perm(
                'establecimientos.download_reporte_global'):
            raise PermissionDenied
        self.filename = self.filename.format(
            request.GET.get('start_date'), request.GET.get('end_date', ''))
        return super(GlobalReportView, self).dispatch(request, *args, **kwargs)

    def get_book(self, output):
        report = GlobalReport(
            self.establecimiento_ids, self.start_date, self.end_date)
        return report.get_book(output)


class LibroRegistroDiarioSeguimientoGestantesReportView(EstablecimientoRequiredMixin, ExcelView):
    filename = 'libro-de-registro-diario-de-seguimiento-de-gestantes-'
    filename += '{}-{}.xlsx'
    establecimiento_ids = []
    start_date = None
    end_date = None

    def dispatch(self, request, *args, **kwargs):
        self.start_date = datetime.strptime(
            request.GET.get('start_date', ''), DATE_FORMAT)
        self.end_date = datetime.strptime(
            request.GET.get('end_date', ''), DATE_FORMAT)
        self.establecimiento_ids = request.GET.getlist(
            'establecimientos', [request.session['establecimiento_id']])
        if len(self.establecimiento_ids) > 1 and \
            not request.user.has_perm(
                'establecimientos.download_reporte_registro_diario_gestaciones'):
            raise PermissionDenied
        self.filename = self.filename.format(
            request.GET.get('start_date'), request.GET.get('end_date', ''))
        return super(
            LibroRegistroDiarioSeguimientoGestantesReportView, self).dispatch(
            request, *args, **kwargs)

    def get_book(self, output):
        report = LibroRegistroDiarioSeguimientoGestantesReport(
            self.start_date, self.end_date, self.establecimiento_ids)
        return report.get_book(output)


def get_json_establecimientos(request, query):
    establecimientos = Establecimiento.objects.filter(
        nombre__icontains=query)[:20]
    p = [
        {"name": "%s - %s - %s" % (establecimiento.codigo, establecimiento.nombre, establecimiento.diresa.nombre),
         "id": establecimiento.id} for establecimiento in establecimientos]
    return JsonResponse(p, safe=False)


class GlobalReportPartoView(EstablecimientoRequiredMixin, ExcelView):
    filename = 'informe-de-{}-a-{}.xlsx'
    establecimiento_ids = []
    start_date = None
    end_date = None

    def get(self, request, *args, **kwargs):
        try:
            self.start_date = datetime.strptime(request.GET.get('start_date', ''), DATE_FORMAT)
        except ValueError:
            messages.warning(request, 'No se ha ingresado una fecha inicial válida: {}'.format(
                            request.GET.get('start_date')))
            return HttpResponseRedirect('/')
        try:
            self.end_date = datetime.strptime(request.GET.get('end_date', ''), DATE_FORMAT)
        except ValueError:
            messages.warning(request, 'No se ha ingresado una fecha inicial válida: {}'.format(
                            request.GET.get('end_date')))
            return HttpResponseRedirect('/')
        self.establecimiento_ids = request.GET.getlist('establecimientos', [request.session['establecimiento_id']])
        if len(self.establecimiento_ids) > 1 and not request.user.has_perm('establecimientos.download_reporte_global'):
            raise PermissionDenied
        self.filename = self.filename.format(request.GET.get('start_date'), request.GET.get('end_date', ''))
        return super(GlobalReportPartoView, self).get(request, *args, **kwargs)

    def get_book(self, output):
        report = GlobalReportParto(
            self.establecimiento_ids, self.start_date, self.end_date)
        return report.get_book(output)


class GlobalReportPuerperioView(EstablecimientoRequiredMixin, ExcelView):
    filename = 'informe-de-{}-a-{}.xlsx'
    establecimiento_ids = []
    start_date = None
    end_date = None

    def get(self, request, *args, **kwargs):
        try:
            self.start_date = datetime.strptime(request.GET.get('start_date', ''), DATE_FORMAT)
        except ValueError:
            messages.warning(request, 'No se ha ingresado una fecha inicial válida: {}'.format(
                            request.GET.get('start_date')))
            return HttpResponseRedirect('/')
        try:
            self.end_date = datetime.strptime(request.GET.get('end_date', ''), DATE_FORMAT)
        except ValueError:
            messages.warning(request, 'No se ha ingresado una fecha inicial válida: {}'.format(
                            request.GET.get('end_date')))
            return HttpResponseRedirect('/')
        self.establecimiento_ids = request.GET.getlist('establecimientos', [request.session['establecimiento_id']])
        if len(self.establecimiento_ids) > 1 and not request.user.has_perm('establecimientos.download_reporte_global'):
            raise PermissionDenied
        self.filename = self.filename.format(request.GET.get('start_date'), request.GET.get('end_date', ''))
        return super(GlobalReportPuerperioView, self).get(request, *args, **kwargs)

    def get_book(self, output):
        report = GlobalReportPuerperio(self.establecimiento_ids, self.start_date, self.end_date)
        return report.get_book(output)