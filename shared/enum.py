from django.db import models


class StatutGeneral(models.TextChoices):
    BROUILLON = 'Brouillon'
    VALIDE = 'Validé'
    SUPPRIME = 'Supprimé'
    ENATTENTE = 'En Attente'


class SituationMatrimoniale(models.TextChoices):
    CELIBATAIRE = 'Célibataire'
    FIANCE = 'Fiancé(e)'
    CONCUBINAGE = 'Concubinage'
    DIVORCE = 'Divorcé(e)'
    MARIE = 'Marié(e)'
    VEUF = 'Veuf(ve)'


class ReponseEnum(models.TextChoices):
    VRAI = 'Vrai'
    FAUX = 'Faux'


class StatutCertificat(models.TextChoices):
    DISPONIBLE = 'Disponible'
    NON_DISPONIBLE = 'Non disponible'


class SessionStatut(models.TextChoices):
    ENATTENTE = 'En attente'
    ENCOURS = 'En cours'
    TERMINE = 'Terminé'


class UserCompteStatut(models.TextChoices):
    ACTIVE = 'Activé'
    DESACTIVE = 'Désactivé'
    FERME = 'Fermé'
    BLOQUE = 'Bloqué'


class Genre(models.TextChoices):
    FEMME = 'Femme'
    HOMME = 'Homme'