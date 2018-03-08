# coding: utf-8
from StringIO import StringIO
from celery.task import task
from django.core.files.uploadedfile import InMemoryUploadedFile


@task
def process_global_report(global_report, report_object):
    output = StringIO()
    book = global_report.get_book(output)
    book.close()
    report_object.file = InMemoryUploadedFile(
        output, report_object.filename, report_object.filename,
        report_object.content_type, output.len, 'utf-8')
    report_object.status = 'done'
    report_object.save()
