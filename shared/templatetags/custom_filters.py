from django import template
from shared.helpers import format_milles, convert_date_any_format

register = template.Library()


@register.filter
def convert_date_format(value):
    return convert_date_any_format(value)


@register.filter
def format_mille(value):
    return format_milles(value)
