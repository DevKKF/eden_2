from datetime import datetime


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