from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for the custom User model (email login)."""

    # Fields to display in the list view
    list_display = ("email", "first_name", "last_name", "phone", "is_recruiter", "is_staff", "is_superuser")
    list_filter = ("is_staff", "is_superuser", "is_recruiter", "is_active")
    search_fields = ("email", "first_name", "last_name", "phone")
    ordering = ("email",)

    # Use email instead of username
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "phone")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "is_recruiter", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    # Add user form for creating new users
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_recruiter", "is_staff", "is_superuser"),
            },
        ),
    )

    # Important: tell Django not to expect a username field
    add_form_template = None
    change_user_password_template = None
