import uuid
from django.db import models
import datetime

from parametre.models import TypeCours
from shared.enum import SessionStatut, StatutGeneral, ReponseEnum, StatutCertificat
from shared.models.base import TimeStampedAuditModel


class Session(TimeStampedAuditModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.TextField(blank=True)
    description = models.TextField(blank=True, null=True)
    date_publication = models.DateField(blank=True, null=True, auto_now=False)
    date_debut = models.DateField(blank=True)
    date_fin = models.DateField(blank=True)
    statut_session = models.fields.CharField(choices=SessionStatut.choices, default=SessionStatut.ENCOURS, max_length=20, null=True)

    def __str__(self):
        return self.nom

    def nombre_certificats(self):
        nombre = Certificat.objects.count()
        return nombre

    def nombre_cours(self):
        nombre = Cours.objects.count()
        return nombre

    class Meta:
        db_table = 'sessions'
        verbose_name = 'Sessions'
        verbose_name_plural = "Sessions"


class Certificat(TimeStampedAuditModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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


def upload_modele_certificat(instance, filename):
    filebase, extension = filename.rsplit('.', 1)
    file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    if filename.startswith('modele_certificat_'):
        return f'certificat/modeles/{filename}'
    return 'certificats/%s.%s' % (file_name, extension)


class ModeleCertificat(TimeStampedAuditModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom_modele = models.TextField(blank=True, null=True)
    date_publication = models.DateField(blank=True, null=True, auto_now=False)
    modele_certificat = models.FileField(upload_to=upload_modele_certificat, null=True, blank=True)
    session = models.ForeignKey(Session, null=True, on_delete=models.RESTRICT, related_name="modele_certificat_sessions")

    def __str__(self):
        return self.nom_modele

    class Meta:
        db_table = 'modele_certificats'
        verbose_name = 'Modeles Certificats'
        verbose_name_plural = "Modeles Certificats"


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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    numero_cours = models.CharField(max_length=50, blank=True, null=True, unique=True)
    titre = models.TextField(blank=True, null=True)
    sous_titre = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date_publication = models.DateField(blank=True, null=True, auto_now=False)
    date_activation = models.DateField(blank=True, null=True, auto_now=False)
    cours_video = models.FileField(upload_to=upload_videos, null=True, blank=True)
    cours_audio = models.FileField(upload_to=upload_audios, null=True, blank=True)
    cours_texte = models.FileField(upload_to=upload_textes, null=True, blank=True)
    type_cours = models.ForeignKey(TypeCours, null=True, on_delete=models.RESTRICT)
    session = models.ForeignKey(Session, null=True, on_delete=models.RESTRICT, related_name="sessions")
    statut_cours = models.fields.CharField(choices=SessionStatut.choices, default=SessionStatut.ENATTENTE, max_length=20, null=True)

    def __str__(self):
        return self.titre

    def liste_qcm(self):
        liste = Question.objects.get()
        return liste

    def nombre_questions(self):
        nombre = Question.objects.count()
        return nombre

    class Meta:
        db_table = 'cours'
        verbose_name = 'Cours'
        verbose_name_plural = "Cours"


class Question(TimeStampedAuditModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    libelle = models.TextField(blank=True, null=True)
    date_publication = models.DateField(blank=True, null=True, auto_now=False)
    point = models.IntegerField(null=True)
    cours = models.ForeignKey(Cours, null=True, on_delete=models.RESTRICT, related_name="cours")
    statut_question = models.fields.CharField(choices=StatutGeneral.choices, default=StatutGeneral.VALIDE, max_length=20, null=True)
    
    def __str__(self):
        return self.libelle

    def liste_reponse(self):
        liste = Reponse.objects.get()
        return liste

    class Meta:
        db_table = 'questions'
        verbose_name = 'Questions'
        verbose_name_plural = "Questions"


class Reponse(TimeStampedAuditModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    libelle = models.TextField(blank=True, null=True)
    point = models.IntegerField(null=True)
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    utilisateur = models.ForeignKey("utilisateur.Utilisateur", null=True, on_delete=models.RESTRICT, related_name="utilisateur")
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    utilisateur = models.ForeignKey("utilisateur.Utilisateur", null=True, on_delete=models.RESTRICT, related_name="participation_utilisateurs")
    cours = models.ForeignKey(Cours, null=True, on_delete=models.RESTRICT, related_name="inscription_cours")
    statut_participation = models.fields.CharField(choices=SessionStatut.choices, default=SessionStatut.ENCOURS, max_length=20, null=True)

    def __str__(self):
        return self.utilisateur

    class Meta:
        db_table = 'participation_cours'
        verbose_name = 'Participations Cours'
        verbose_name_plural = "Participations Cours"


class ReponseUtilisateur(TimeStampedAuditModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_heure_debut = models.DateTimeField(blank=True, null=True, auto_now=False)
    date_heure_fin = models.DateTimeField(blank=True, null=True, auto_now=False)
    point_acquis = models.IntegerField(null=True)
    utilisateur = models.ForeignKey("utilisateur.Utilisateur", null=True, on_delete=models.RESTRICT, related_name="reponse_utilisateurs")
    question = models.ForeignKey(Question, null=True, on_delete=models.RESTRICT, related_name="question_reponses")
    reponse = models.ForeignKey(Reponse, null=True, on_delete=models.RESTRICT, related_name="reponse_questions")

    def __str__(self):
        return self.question

    class Meta:
        db_table = 'reponse_utilisateurs'
        verbose_name = 'Reponses Utilisateurs'
        verbose_name_plural = "Reponses Utilisateurs"
