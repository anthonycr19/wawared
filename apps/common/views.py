# coding:utf-8
from StringIO import StringIO

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View
from reportlab.pdfgen.canvas import Canvas


class LoginRequiredMixin(object):
    permissions = ()

    @method_decorator(login_required(login_url='/ingresar/'))
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perms(self.permissions):
            raise PermissionDenied
        return super(
            LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class PdfView(View):
    filename = ''

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename={}'.format(self.filename)
        c = Canvas(response)
        c = self.process_canvas(c)
        c.save()
        return response

    def process_canvas(self, _canvas):
        raise NotImplementedError


class ExcelView(View):
    """
    Return xlwt WorkBook
    """
    filename = ''

    def get(self, request, *args, **kwargs):
        output = StringIO()
        book = self.get_book(output)
        book.close()
        output.seek(0)
        response = HttpResponse(
            output.read(), content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename={}'.format(
            self.filename)
        return response

    def get_book(self, output):
        raise NotImplementedError
