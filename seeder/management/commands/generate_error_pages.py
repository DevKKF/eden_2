import os
from django.core.management.base import BaseCommand
from django.conf import settings

ERROR_CODES = [400, 401, 402, 403, 404, 419, 429, 500, 503]

BASE_HTML_CONTENT = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Erreur{% endblock %}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f8f8f8;
            text-align: center;
            padding-top: 100px;
        }}
        h1 {{
            font-size: 60px;
            color: #d9534f;
        }}
        p {{
            font-size: 20px;
        }}
    </style>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
"""

TEMPLATE_CONTENT = """{{% extends "base.html" %}}

{{% block content %}}
<h1>{code} - Erreur</h1>
<p>Une erreur {code} est survenue.</p>
{{% endblock %}}
"""

class Command(BaseCommand):
    help = "Génère des templates HTML personnalisés pour les erreurs HTTP"

    def handle(self, *args, **options):
        templates_dir = os.path.join(settings.BASE_DIR, 'templates', 'errors')
        os.makedirs(templates_dir, exist_ok=True)

        # Génération de base.html
        base_html_path = os.path.join(templates_dir, 'base.html')
        if not os.path.exists(base_html_path):
            with open(base_html_path, 'w', encoding='utf-8') as f:
                f.write(BASE_HTML_CONTENT)
            self.stdout.write(self.style.SUCCESS("✔ base.html généré."))

        for code in ERROR_CODES:
            file_path = os.path.join(templates_dir, f"{code}.html")
            if not os.path.exists(file_path):
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(TEMPLATE_CONTENT.format(code=code))
                self.stdout.write(self.style.SUCCESS(f"✔ {code}.html généré"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠ {code}.html existe déjà"))
