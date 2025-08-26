from datetime import datetime

from datetime import datetime

def convert_date_any_format(date_str):
    try:
        return datetime.strptime(date_str, '%d/%m/%Y').date()
    except (ValueError, TypeError):
        return None