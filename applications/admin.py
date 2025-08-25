from django.contrib import admin
from .models import Application, ApplicationEvent
@admin.register(ApplicationEvent)
class ApplicationEventAdmin(admin.ModelAdmin):
    list_display = ("application", "event", "created_at")
    list_filter = ("event", "created_at")
    search_fields = ("application__job__title", "application__applicant__email", "event", "note")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")


