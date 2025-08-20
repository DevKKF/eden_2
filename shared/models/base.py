from django.db import models

from shared.models.audit import AuditModel


class BaseModel(models.Model):
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class TimeStampedAuditModel(BaseModel, AuditModel):
    class Meta:
        abstract = True

