from django.contrib import admin
from .models import Job, JobCategory

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "category", "employment_type", "experience_level", "location_type", "created_at")
    list_filter = ("employment_type", "experience_level", "location_type", "country", "created_at")
    search_fields = ("title", "company__name", "category__name")
    autocomplete_fields = ("company", "category", "skills")

@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")  
    search_fields = ("name",)
    list_filter = ("is_active", "created_at")


