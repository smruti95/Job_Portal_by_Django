from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from common.models import UUIDModel, TimeStampedModel
from common.choices import NotificationType
from accounts.models import User

class Notification(UUIDModel, TimeStampedModel):
    recipient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="notifications",
        db_index=True, 
        verbose_name="recipient"
    )
    type = models.CharField(
        max_length=20, 
        choices=NotificationType.choices, 
        db_index=True
    )
    verb = models.CharField(
        max_length=160, 
        help_text="Action phrase, e.g., 'updated your application'"
    )
    # Generic relation to any object (Job, Application, etc.)
    target_ct = models.ForeignKey(
        ContentType, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    target_id = models.CharField(
        max_length=64, 
        null=True, 
        blank=True)
    target = GenericForeignKey("target_ct", "target_id")
    is_read = models.BooleanField(default=False, db_index=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "notification"
        verbose_name_plural = "notifications"
        indexes = [
            models.Index(fields=["recipient", "is_read"], name="notif_recipient_read_idx"),
            models.Index(fields=["type", "created_at"], name="notif_type_created_idx"),
        ]
