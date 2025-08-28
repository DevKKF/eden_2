from django.utils import timezone

from session.models import Session
from shared.enum import SessionStatut


def run_sessions(created_by_user):
    """
    Insère les données de base pour les sessions, en utilisant l'utilisateur fourni
    pour le champ 'created_by'.
    """
    # Exemple pour les sessions
    session_data = [
        {"nom": "Session de formation de Janvier - Juin 2025 ", "description": "Session de formation de Janvier - Juin 2025", "date_publication": "2025-08-27", "date_debut": "2025-01-01", "date_fin": "2025-06-30"},
    ]
    for data in session_data:
        Session.objects.get_or_create(
            nom=data["nom"],
            description=data["description"],
            date_publication=data["date_publication"],
            date_debut=data["date_debut"],
            date_fin=data["date_fin"],
            statut_session=SessionStatut.ENCOURS,
            created_by=created_by_user.pk,
            created_at=timezone.now()
        )

    print("✅  Sessions insérées avec succès.")
