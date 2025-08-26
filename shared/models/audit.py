from django.db import models
from django.conf import settings
from django.utils import timezone

from middleware.current_user import get_current_user

class AuditModel(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.RESTRICT, related_name="created_%(class)s_set")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.RESTRICT, related_name="updated_%(class)s_set")
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.RESTRICT, related_name="deleted_%(class)s_set")

    def save(self, *args, **kwargs):
        user = get_current_user()
        is_create = self._state.adding  # True si création, False si update

        if is_create and not self.created_by:
            self.created_by = user

        self.updated_by = user
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        """Soft delete : marque l’objet comme supprimé sans le retirer de la DB"""
        user = get_current_user()
        self.deleted_by = user
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_by", "deleted_at"])

    class Meta:
        abstract = True

