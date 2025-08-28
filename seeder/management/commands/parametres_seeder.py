from django.utils import timezone

from parametre.models import Departement, Tribu, Quartier, TypeCours


def run_parametres(created_by_user):
    """
    Insère les données de base pour les paramètres, en utilisant l'utilisateur fourni
    pour le champ 'created_by'.
    """
    # Exemple pour les departements
    departement_data = [
        {"libelle": "Portiers"},
        {"libelle": "Protocole"},
        {"libelle": "Amie Des Nouveaux"},
        {"libelle": "Sainte-Cène"},
        {"libelle": "Gestion des Cultes"},
        {"libelle": "Com"},
        {"libelle": "Sono"},
    ]
    for data in departement_data:
        Departement.objects.get_or_create(
            libelle=data["libelle"],
            created_by=created_by_user.pk,
            created_at=timezone.now()
        )

    # Exemple pour les tribus
    tribus = [
        {"libelle": "Zabulon"},
        {"libelle": "Siméon"},
        {"libelle": "Nephthali"},
        {"libelle": "Lévi"},
        {"libelle": "Aser"},
        {"libelle": "Ruben"},
        {"libelle": "Gad"},
        {"libelle": "Joseph"},
        {"libelle": "Dan"},
        {"libelle": "Benjamin"},
        {"libelle": "Juda"},
        {"libelle": "Issacar"},
    ]
    for data in tribus:
        Tribu.objects.get_or_create(
            libelle=data["libelle"],
            created_by=created_by_user.pk,
            created_at=timezone.now()
        )

    # Exemple pour les quartiers
    quartier_data = [
        {"libelle": "Dokui - Alocodrone"},
        {"libelle": "Dokui - Petit Marché"},
    ]
    for data in quartier_data:
        Quartier.objects.get_or_create(
            libelle=data["libelle"],
            created_by=created_by_user.pk,
            created_at=timezone.now()
        )

    # Exemple pour les types de cours
    type_cours_data = [
        {"code": "VIDEOS", "libelle": "Vidéos"},
        {"code": "AUDIOS", "libelle": "Audios"},
        {"code": "TEXTES", "libelle": "Textes"},
    ]
    for type_cours in type_cours_data:
        TypeCours.objects.get_or_create(
            code=type_cours["code"],
            libelle=type_cours["libelle"],
            created_by=created_by_user.pk,
            created_at=timezone.now()
        )

    print("✅  Paramètres insérés avec succès.")
