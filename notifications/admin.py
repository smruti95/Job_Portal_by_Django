from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("recipient", "verb", "type", "is_read", "created_at")
    list_filter = ("is_read", "type", "created_at")
    search_fields = ("recipient__email", "verb")

