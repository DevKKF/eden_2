from django import template
from shared.helpers import format_milles, convert_date_any_format

register = template.Library()


@register.filter
def convert_date_format(value):
    return convert_date_any_format(value)


@register.filter
def format_mille(value):
    return format_milles(value)


@register.filter
def in_list(value, arg):
    """Vérifie si la valeur est dans une liste séparée par des virgules"""
    return value in [x.strip() for x in arg.split(',')]

