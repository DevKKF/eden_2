import os
import re
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = "Vérifie que tous les fichiers {% static '...' %} référencés existent bien"

    def handle(self, *args, **kwargs):
        static_pattern = re.compile(r"{%\s*static\s*['\"]([^'\"]+)['\"]\s*%}")
        static_root = os.path.join(settings.BASE_DIR, 'static')

        total = 0
        missing = 0

        for root, _, files in os.walk(os.path.join(settings.BASE_DIR, 'templates')):
            for file in files:
                if file.endswith(".html"):
                    path = os.path.join(root, file)
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                        matches = static_pattern.findall(content)
                        for relative_path in matches:
                            total += 1
                            full_path = os.path.join(static_root, relative_path)
                            if not os.path.exists(full_path):
                                self.stdout.write(self.style.ERROR(f"❌ Manquant : {relative_path} référencé dans {path}"))
                                missing += 1

        self.stdout.write(self.style.SUCCESS(f"\nTotal référencés : {total}"))
        self.stdout.write(self.style.SUCCESS(f"Manquants       : {missing}"))
        if missing == 0:
            self.stdout.write(self.style.SUCCESS("✅  Tous les fichiers statiques sont présents !"))
        else:
            self.stdout.write(self.style.WARNING("⚠️  Des fichiers statiques sont manquants."))
