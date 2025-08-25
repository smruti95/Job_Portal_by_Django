from rest_framework import serializers
from .models import Job, JobCategory, Skill
from django.utils import timezone

class JobSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(), many=True, required=False
    )

    class Meta:
        model = Job
        fields = [
            "id", "company", "title", "slug", "description",
            "category", "experience_level", "employment_type",
            "location_type", "country", "city", "min_salary", "max_salary",
            "application_deadline", "published_at", "skills", "is_active",
            "created_at", "updated_at"
        ]
        read_only_fields = ["id", "slug", "published_at", "created_at", "updated_at"]

    def validate(self, data):
        min_salary = data.get("min_salary")
        max_salary = data.get("max_salary")
        if min_salary and max_salary and min_salary > max_salary:
            raise serializers.ValidationError("Minimum salary cannot be greater than maximum salary.")

        
        deadline = data.get("application_deadline")
        if deadline and deadline < timezone.now().date():
            raise serializers.ValidationError("Application deadline cannot be in the past.")

        # Location validation
        location_type = data.get("location_type")
        country = data.get("country")
        city = data.get("city")
        if location_type == "ONSITE" and (not country or not city):
            raise serializers.ValidationError("Onsite jobs must have both city and country.")
        if location_type == "REMOTE" and (country or city):
            raise serializers.ValidationError("Remote jobs should not have city or country filled.")

        return data
