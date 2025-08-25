from django.db import models
from django.db.models import Q
from common.models import UUIDModel, TimeStampedModel
from common.choices import ApplicationStatus
from accounts.models import User
from jobs.models import Job

class Application(UUIDModel, TimeStampedModel):
    job = models.ForeignKey(
        Job, 
        on_delete=models.CASCADE, 
        related_name="applications",
        verbose_name="job", 
        help_text="Job being applied for.")
    applicant = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="applications",
        verbose_name="applicant", 
        help_text="User who submitted the application.")
    resume_snapshot = models.FileField(
        upload_to="applications/%Y/%m/",
        blank=True, 
        null=True, 
        help_text="Optional resume copy uploaded specifically for this application.")
    cover_letter = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, 
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.SUBMITTED, 
        db_index=True)

    class Meta:
        verbose_name = "application"
        verbose_name_plural = "applications"
        constraints = [
            models.UniqueConstraint(fields=["job", "applicant"], name="unique_job_applicant"),
        ]
        indexes = [
            models.Index(fields=["job", "status"], name="app_job_status_idx"),
            models.Index(fields=["applicant", "created_at"], name="app_applicant_created_idx"),
        ]

    def __str__(self):
        return f"{self.applicant.email} → {self.job.title}"

class ApplicationEvent(UUIDModel, TimeStampedModel):
    application = models.ForeignKey(
        Application, 
        on_delete=models.CASCADE, 
        related_name="events")
    event = models.CharField(
        max_length=80, 
        help_text="e.g., Status changed, Note added")
    note = models.TextField(blank=True)

    class Meta:
        verbose_name = "application event"
        verbose_name_plural = "application events"
        indexes = [models.Index(fields=["application", "created_at"], name="appevent_app_created_idx")]
