from datetime import datetime
from django.apps import apps
from django.db.models import Q


def relation_entre_table(obj):
    """
    Vérifie si un objet est référencé dans une autre table
    (via ForeignKey ou ManyToMany).
    """
    for rel in obj._meta.related_objects:
        accessor_name = rel.get_accessor_name()
        related_manager = getattr(obj, accessor_name)

        if related_manager.exists():
            return True
    return False


def convert_date_any_format(date_str):
    try:
        return datetime.strptime(date_str, '%d/%m/%Y').date()
    except (ValueError, TypeError):
        return None


def format_milles(number):
    try:
        return f"{number:,.0f}".replace(",", ".")
    except (ValueError, TypeError):
        return None

