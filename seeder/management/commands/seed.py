from django.core.management.base import BaseCommand

from seeder.management.commands.parametres_seeder import run_parametres
from seeder.management.commands.session import run_sessions
from seeder.management.commands.utilisateurs_seeder import run_utilisateurs


class Command(BaseCommand):
    help = 'Insère les données de référence (paramètres, utilisateur, etc.)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("🚀  Début du seed..."))

        # Exécuter le seed des utilisateurs et récupérer l'objet utilisateur
        user_admin = run_utilisateurs()

        # Exécuter le seed des paramètres, en passant l'utilisateur admin
        run_parametres(user_admin)

        # Exécuter le seed des sessions, en passant l'utilisateur admin
        run_sessions(user_admin)

        self.stdout.write(self.style.SUCCESS("✅  Seed terminé avec succès."))

