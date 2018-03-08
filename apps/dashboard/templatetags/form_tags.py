# coding: utf-8

from django import template
from django.template import loader, Context

register = template.Library()


@register.simple_tag()
def cie_select(field):
    _context = Context({
        'field': field
    })
    _template = loader.get_template('dashboard/partials/cie_select_js.html')
    return _template.render(_context)


@register.simple_tag()
def establecimiento_select(field):
    _context = Context({
        'field': field
    })
    _template = loader.get_template(
        'dashboard/partials/establecimiento_select_js.html')
    return _template.render(_context)
