import os
from django.db.models.signals import post_delete
from django.dispatch import receiver

from session.models import Cours


@receiver(post_delete, sender=Cours)
def supprimer_fichiers_cours(sender, instance, **kwargs):
    """Supprime les fichiers associés quand un cours est supprimé"""
    champs_fichiers = ['cours_video', 'cours_audio', 'cours_texte']

    for champ in champs_fichiers:
        fichier = getattr(instance, champ)
        if fichier and fichier.path and os.path.isfile(fichier.path):
            try:
                os.remove(fichier.path)
            except Exception:
                pass