import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

from parametre.models import Departement, Tribu, Quartier
from shared.enum import SituationMatrimoniale, UserCompteStatut, Genre


def upload_photo(instance, filename):
    filebase, extension = filename.rsplit('.', 1)
    file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    if filename.startswith('photo_'):
        return f'utilisateur/profil/{filename}'
    return 'profil/%s.%s' % (file_name, extension)


class Utilisateur(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    numero_utilisateur = models.CharField(max_length=20, blank=True, null=True, unique=True)
    nom = models.CharField(max_length=20, blank=True, default=None, null=True)
    prenoms = models.CharField(max_length=80, blank=True, default=None, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    autre_telephone = models.CharField(max_length=20, blank=True, null=True)
    indicatif_telephonique = models.CharField(max_length=20, blank=True, null=True, default='+225')
    date_naissance = models.DateField(max_length=20, blank=True, null=True)
    situation_matrimoniale = models.fields.CharField(choices=SituationMatrimoniale.choices, default=SituationMatrimoniale.CELIBATAIRE, max_length=20, null=True)
    sexe = models.fields.CharField(choices=Genre.choices, default=None, max_length=20, null=True)
    tribu = models.ForeignKey(Tribu, null=True, on_delete=models.RESTRICT)
    departement = models.ForeignKey(Departement, null=True, on_delete=models.RESTRICT)
    quartier = models.ForeignKey(Quartier, null=True, on_delete=models.RESTRICT)
    certificat = models.ForeignKey("session.Certificat", null=True, on_delete=models.RESTRICT)
    session = models.ForeignKey("session.Session", null=True, on_delete=models.RESTRICT)
    photo = models.ImageField(upload_to=upload_photo, null=True, blank=True)
    statut_compte = models.fields.CharField(choices=UserCompteStatut.choices, default=UserCompteStatut.ACTIVE, max_length=20, null=True)

    class Meta:
        db_table = 'utilisateurs'
        verbose_name = "Utilisateurs"
        verbose_name_plural = "Utilisateurs"

    @property
    def is_superadmin(self):
        if self.groups.filter(name__contains='SUPERADMIN').first() is not None:
            return True
        return False

    @property
    def is_admin(self):
        if self.groups.filter(name__contains='ADMIN').first() is not None:
            return True
        return False

    @property
    def is_utilisateur(self):
        if self.groups.filter(name__contains='UTILISATEUR').first() is not None:
            return True
        return False

    def __str__(self):
        return f'{self.nom} {self.prenoms}'

