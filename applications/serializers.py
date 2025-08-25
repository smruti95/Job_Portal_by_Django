from rest_framework import serializers
from .models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            "id", "job", "applicant", "resume_snapshot",
            "cover_letter", "status", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "status", "created_at", "updated_at"]
