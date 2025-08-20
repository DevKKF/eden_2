from django.db import models

from shared.models.base import TimeStampedAuditModel


class Quartier(TimeStampedAuditModel):
    libelle = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.libelle

    class Meta:
        db_table = 'quartiers'
        verbose_name = 'Quartiers'
        verbose_name_plural = "Quartiers"

class Departement(TimeStampedAuditModel):
    libelle = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.libelle

    class Meta:
        db_table = 'departements'
        verbose_name = 'Departements'
        verbose_name_plural = "Departements"

class Tribu(TimeStampedAuditModel):
    libelle = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.libelle

    class Meta:
        db_table = 'tribus'
        verbose_name = 'Tribus'
        verbose_name_plural = "Tribus"

class TypeCours(TimeStampedAuditModel):
    libelle = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.libelle

    class Meta:
        db_table = 'type_cours'
        verbose_name = 'Types de cours'
        verbose_name_plural = "Types de cours"
