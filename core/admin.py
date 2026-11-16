from django.contrib import admin

from .models import ContactSubmission


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("full_name", "organization", "email", "inquiry_type", "submitted_at")
    list_filter = ("inquiry_type", "submitted_at")
    search_fields = ("full_name", "organization", "email", "message")
    ordering = ("-submitted_at",)
    readonly_fields = ("submitted_at",)
    date_hierarchy = "submitted_at"
