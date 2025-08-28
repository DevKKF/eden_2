import uuid
from django.db import models
from django.utils import timezone

from middleware.current_user import get_current_user

class AuditModel(models.Model):
    created_by = models.UUIDField(editable=False, null=True, blank=True)
    updated_by = models.UUIDField(editable=False, null=True, blank=True)
    deleted_by = models.UUIDField(editable=False, null=True, blank=True)

    class Meta:
        abstract = True
