from shared.enum import SituationMatrimoniale
from utilisateur.models import Utilisateur
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.contrib.auth.models import Permission


def ajouter_permissions_app_au_groupe(nom_app, groupe):
    """
    Ajoute toutes les permissions d'une application à un groupe.
    """
    models = apps.get_app_config(nom_app).get_models()
    for model in models:
        content_type = ContentType.objects.get_for_model(model)
        permissions = Permission.objects.filter(content_type=content_type)
        groupe.permissions.add(*permissions)
    print(f"✅  Permissions de l'app '{nom_app}' ajoutées.")


def run_utilisateurs():
    """
    Crée ou récupère l'utilisateur administrateur et le groupe SUPERADMIN.
    Retourne l'objet utilisateur créé.
    """
    # Créer ou récupérer l'utilisateur pasteurtanoh@gmail.com
    user, created = Utilisateur.objects.get_or_create(username='pasteurtanoh@gmail.com')
    if created:
        user.nom = 'Pasteur Tanoh'
        user.prenoms = 'Laurent'
        user.first_name = 'Pasteur Tanoh'
        user.last_name = 'Laurent'
        user.email = 'pasteurtanoh@gmail.com'
        user.telephone = '0574418372'
        user.situation_matrimoniale = SituationMatrimoniale.MARIE
        user.is_superuser = True
        user.is_staff = True
        user.set_password('P@sswordPTL')
        user.save()
        print("✅  Utilisateur admin créé.")
    else:
        print("ℹ️  Utilisateur admin déjà existant.")

    print("✅  Utilisateur lié au groupe SUPERADMIN.")

    return user

