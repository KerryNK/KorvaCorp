from django.db import models


class ContactSubmission(models.Model):
    class InquiryType(models.TextChoices):
        STRATEGIC_PARTNERSHIP = "strategic_partnership", "Strategic partnership"
        CAPITAL_ALIGNMENT = "capital_alignment", "Capital alignment"
        MEDIA_PUBLIC_RELATIONS = "media_public_relations", "Media or public relations"
        OPERATIONAL_COLLABORATION = "operational_collaboration", "Operational collaboration"

    full_name = models.CharField(max_length=150)
    organization = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    inquiry_type = models.CharField(max_length=40, choices=InquiryType.choices)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]
        verbose_name = "contact submission"
        verbose_name_plural = "contact submissions"

    def __str__(self):
        return f"{self.full_name} — {self.get_inquiry_type_display()}"
