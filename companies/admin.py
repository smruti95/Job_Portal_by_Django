from django.contrib import admin
from .models import Company, CompanyMember

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "owner", "industry", "city", "country", "verified", "is_active")
    list_filter = ("industry", "country", "verified", "is_active")
    search_fields = ("name", "owner__email", "city", "country")
    prepopulated_fields = {"slug": ("name",)}   # auto-fill slug from name
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")  # from TimeStampedModel

@admin.register(CompanyMember)
class CompanyMemberAdmin(admin.ModelAdmin):
    list_display = ("user", "company", "role", "created_at")
    list_filter = ("role", "company__industry", "company__country")
    search_fields = ("user__email", "company__name")
    ordering = ("company", "user")
    readonly_fields = ("created_at", "updated_at")

