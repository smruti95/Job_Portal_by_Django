from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id", "recipient", "type", "verb",
            "target_ct", "target_id", "is_read", "read_at",
            "created_at", "updated_at"
        ]
        read_only_fields = ["id", "is_read", "read_at", "created_at", "updated_at"]
