import requests
from cStringIO import StringIO

from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponse, Http404

from firma.models import Document


def print_choices(field, choices):
    def wrapper(self):
        for choice in choices:
            if getattr(self, field) in choice:
                return choice[1]
        return ''

    return wrapper


class BaseJasperReport(object):
    report_name = ''
    filename = ''

    def __init__(self):
        self.auth = (settings.JASPER_USER, settings.JASPER_PASSWORD)
        super(BaseJasperReport, self).__init__()

    def get_report(self):
        url = '{url}{path}/{report_name}.pdf'.format(
            url=settings.JASPER_URL, path=settings.JASPER_PATH,
            report_name=self.report_name)

        req = requests.get(url, params=self.get_params(), auth=self.auth)
        return req.content

    def get_params(self):
        raise NotImplementedError

    def signed_report(self, identifier , path_next):
        # firmar documento
        buffer = self.render_to_buffer()
        try:
            # Devuelve el documento firmado
            doc = Document.objects.get(identifier=identifier,signed_file='')
        except Document.DoesNotExist:
            doc = Document.new('{}_{}.pdf'.format(self.report_name, identifier), identifier, buffer, "pdf")
        return redirect('{}?next={}'.format(reverse('firma:sign-document',
                                                    kwargs={'document_id': doc.id}), path_next))
    def render_signed_file(self, identifier):
        # Devuelve el documento firmado
        qr = Document.objects.filter(identifier=identifier).exclude(signed_file='')
        if qr.count() == 1:
            doc = qr[0]
            response = HttpResponse(content_type='application/pdf')
            response[
                'Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(
                doc.name)
            response.write(doc.signed_file.read())
            return response
        else:
            raise Http404

    def render_to_response(self):
        response = HttpResponse(content_type='application/pdf')
        response[
            'Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(
            self.filename)
        response.write(self.get_report())
        return response

    def render_to_inlineresponse(self):
        response = HttpResponse(content_type='application/pdf')
        response[
            'Content-Disposition'] = 'inline; filename="{}.pdf"'.format(
            self.filename)
        response.write(self.get_report())
        return response

    def render_to_buffer(self):
        buffer = StringIO(self.get_report())
        return buffer

