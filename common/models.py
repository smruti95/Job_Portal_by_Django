from django.db import models
import uuid
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True,
        verbose_name="created at", 
        help_text="When the record was created.")
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="updated at", 
        help_text="When the record was last updated.")

    class Meta:
        abstract = True

class UUIDModel(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False,
        verbose_name="public id", 
        help_text="Stable public UUID identifier.")
    class Meta:
        abstract = True

class Activatable(models.Model):
    is_active = models.BooleanField(default=True, db_index=True,
        verbose_name="active?", help_text="Soft-active flag for the record.")
    class Meta:
        abstract = True
