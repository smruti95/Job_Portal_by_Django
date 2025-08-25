from django.contrib import admin
from .models import Profile, Skill, Education, Experience


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "headline", "location", "updated_at")
    search_fields = ("user__username", "headline", "location")
    list_filter = ("location", "updated_at")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("name",)

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("profile", "institution", "degree", "start_year", "end_year")
    search_fields = ("institution", "degree")

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("profile", "company", "title", "start_date", "end_date")
    search_fields = ("company", "title")
