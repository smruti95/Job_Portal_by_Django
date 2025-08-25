from django.db import models
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()

class AuditLog(models.Model):
    ACTION_CHOICES = (
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=6, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=255)
    object_id = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=now)
    old_data = models.JSONField(blank=True, null=True)   
    new_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.action} on {self.model_name} ({self.object_id}) by {self.user}"
