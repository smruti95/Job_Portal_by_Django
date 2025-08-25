from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "id", "owner", "name", "slug", "website", "industry",
            "size", "city", "country", "about", "verified",
            "created_at", "updated_at"
        ]
        read_only_fields = ["id", "slug", "verified", "created_at", "updated_at"]
