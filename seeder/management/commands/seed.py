from django.core.management.base import BaseCommand
from .parametres_seeder import run as seed_parametres
from .utilisateurs_seeder import run as seed_utilisateurs


class Command(BaseCommand):
    help = 'Insère les données de référence (paramètres, utilisateur, etc.)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("🚀  Début du seed..."))

        seed_parametres()
        seed_utilisateurs()

        self.stdout.write(self.style.SUCCESS("✅  Seed terminé avec succès."))
