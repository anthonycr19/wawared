from django import template

register = template.Library()


@register.filter
def replace(value, argument):
    if argument is None:
        return ''
    arg_list = [arg.strip() for arg in argument.split(' ')]
    return value.replace(arg_list[0], arg_list[1])
