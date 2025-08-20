from django.db import models
import datetime

from parametre.models import TypeCours
from shared.enum import SessionStatut, StatutGeneral, ReponseEnum, StatutCertificat
from shared.models.base import TimeStampedAuditModel
from utilisateur.models import Utilisateur


class Session(TimeStampedAuditModel):
    nom = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date_publication = models.DateField(blank=True, null=True, auto_now=False)
    date_debut = models.DateField(blank=True, null=True, auto_now=False)
    date_fin = models.DateField(blank=True, null=True, auto_now=False)
    statut_session = models.fields.CharField(choices=SessionStatut.choices, default=SessionStatut.ENCOURS, max_length=20, null=True)

    def __str__(self):
        return self.nom

    class Meta:
        db_table = 'sessions'
        verbose_name = 'Sessions'
        verbose_name_plural = "Sessions"


class Certificat(TimeStampedAuditModel):
    numero_certificat = models.CharField(max_length=50, blank=True, null=True, unique=True)
    date_debut_validite = models.DateField(blank=True, null=True, auto_now=False)
    date_fin_validite = models.DateField(blank=True, null=True, auto_now=False)
    date_utilisation = models.DateField(blank=True, null=True, auto_now=False)
    session = models.ForeignKey(Session, null=True, on_delete=models.RESTRICT, related_name="certification_sessions")
    statut_certificat = models.fields.CharField(choices=StatutCertificat.choices, default=StatutCertificat.DISPONIBLE, max_length=20, null=True)

    def __str__(self):
        return self.numero_certificat

    class Meta:
        db_table = 'certificats'
        verbose_name = 'Certificats'
        verbose_name_plural = "Certificats"


def upload_videos(instance, filename):
    filebase, extension = filename.rsplit('.', 1)
    file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    if filename.startswith('videos_'):
        return f'cours/videos/{filename}'
    return 'videos/%s.%s' % (file_name, extension)


def upload_audios(instance, filename):
    filebase, extension = filename.rsplit('.', 1)
    file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    if filename.startswith('audios_'):
        return f'cours/audios/{filename}'
    return 'audios/%s.%s' % (file_name, extension)


def upload_textes(instance, filename):
    filebase, extension = filename.rsplit('.', 1)
    file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    if filename.startswith('textes_'):
        return f'cours/textes/{filename}'
    return 'textes/%s.%s' % (file_name, extension)


class Cours(TimeStampedAuditModel):
    titre = models.CharField(max_length=50, blank=True, null=True)
    sous_titre = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date_publication = models.DateField(blank=True, null=True, auto_now=False)
    cours_video = models.ImageField(upload_to=upload_videos, null=True, blank=True)
    cours_audio = models.ImageField(upload_to=upload_audios, null=True, blank=True)
    cours_texte = models.ImageField(upload_to=upload_textes, null=True, blank=True)
    type_cours = models.ForeignKey(TypeCours, null=True, on_delete=models.RESTRICT)
    session = models.ForeignKey(Session, null=True, on_delete=models.RESTRICT, related_name="sessions")
    statut_cours = models.fields.CharField(choices=SessionStatut.choices, default=SessionStatut.ENCOURS, max_length=20, null=True)

    def __str__(self):
        return self.titre

    class Meta:
        db_table = 'cours'
        verbose_name = 'Cours'
        verbose_name_plural = "Cours"


class Question(TimeStampedAuditModel):
    libelle = models.CharField(max_length=50, blank=True, null=True)
    date_publication = models.DateField(blank=True, null=True, auto_now=False)
    point = models.IntegerField(null=True)
    cours = models.ForeignKey(Cours, null=True, on_delete=models.RESTRICT, related_name="cours")
    statut_question = models.fields.CharField(choices=StatutGeneral.choices, default=StatutGeneral.VALIDE, max_length=20, null=True)
    
    def __str__(self):
        return self.libelle

    class Meta:
        db_table = 'questions'
        verbose_name = 'Questions'
        verbose_name_plural = "Questions"


class Reponse(TimeStampedAuditModel):
    libelle = models.CharField(max_length=50, blank=True, null=True)
    date_publication = models.DateField(blank=True, null=True, auto_now=False)
    question = models.ForeignKey(Question, null=True, on_delete=models.RESTRICT, related_name="questions")
    statut_reponse = models.fields.CharField(choices=ReponseEnum.choices, default=ReponseEnum.VRAI, max_length=20, null=True)

    def __str__(self):
        return self.libelle

    class Meta:
        db_table = 'reponses'
        verbose_name = 'Reponses'
        verbose_name_plural = "Reponses"


class Inscription(TimeStampedAuditModel):
    utilisateur = models.ForeignKey(Utilisateur, null=True, on_delete=models.RESTRICT, related_name="utilisateur")
    session = models.ForeignKey(Session, null=True, on_delete=models.RESTRICT, related_name="inscription_sessions")
    certificat = models.ForeignKey(Certificat, null=True, on_delete=models.RESTRICT, related_name="inscription_certificats")
    statut_inscription = models.fields.CharField(choices=SessionStatut.choices, default=SessionStatut.ENCOURS, max_length=20, null=True)

    def __str__(self):
        return self.utilisateur

    class Meta:
        db_table = 'inscriptions'
        verbose_name = 'Inscriptions'
        verbose_name_plural = "Inscriptions"


class ParticipationCours(TimeStampedAuditModel):
    utilisateur = models.ForeignKey(Utilisateur, null=True, on_delete=models.RESTRICT, related_name="participation_utilisateurs")
    cours = models.ForeignKey(Cours, null=True, on_delete=models.RESTRICT, related_name="inscription_cours")
    statut_participation = models.fields.CharField(choices=SessionStatut.choices, default=SessionStatut.ENCOURS, max_length=20, null=True)

    def __str__(self):
        return self.utilisateur

    class Meta:
        db_table = 'participation_cours'
        verbose_name = 'Participations Cours'
        verbose_name_plural = "Participations Cours"


class ReponseUtilisateur(TimeStampedAuditModel):
    date_heure_debut = models.DateTimeField(blank=True, null=True, auto_now=False)
    date_heure_fin = models.DateTimeField(blank=True, null=True, auto_now=False)
    point_acquis = models.IntegerField(null=True)
    utilisateur = models.ForeignKey(Utilisateur, null=True, on_delete=models.RESTRICT, related_name="reponse_utilisateurs")
    question = models.ForeignKey(Question, null=True, on_delete=models.RESTRICT, related_name="question_reponses")
    reponse = models.ForeignKey(Reponse, null=True, on_delete=models.RESTRICT, related_name="reponse_questions")

    def __str__(self):
        return self.question

    class Meta:
        db_table = 'reponse_utilisateurs'
        verbose_name = 'Reponses Utilisateurs'
        verbose_name_plural = "Reponses Utilisateurs"
