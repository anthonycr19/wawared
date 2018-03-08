from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='integer_to_range')
def integer_to_range(value):
    return xrange(1, value + 1)


@register.filter
def pagination_range(page_obj):
    num_pages = page_obj.paginator.num_pages
    current = page_obj.number
    variation = settings.PAGE_SIZE / 2
    min_value = current - variation
    max_value = current + variation
    if num_pages <= settings.PAGE_SIZE:
        return range(1, num_pages + 1)
    if min_value <= 0:
        return range(1, settings.PAGE_SIZE)
    if max_value >= num_pages:
        return range(num_pages - settings.PAGE_SIZE + 2, num_pages + 1)
    return range(min_value + 1, max_value)
