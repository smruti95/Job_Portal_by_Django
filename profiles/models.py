from django.db import models
from django.core.validators import URLValidator
from common.models import UUIDModel, TimeStampedModel
from common.validators import max_file_size_mb, allowed_extensions, phone_validator
from accounts.models import User
from jobs.models import Skill

class Profile(UUIDModel, TimeStampedModel):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name="profile",
        verbose_name="user", 
        help_text="The account this profile belongs to.")
    headline = models.CharField(
        max_length=160, 
        blank=True, 
        help_text="Short professional title.")
    bio = models.TextField(
        blank=True, 
        help_text="Summary about the candidate.")
    location = models.CharField(
        max_length=120, 
        blank=True)
    website = models.URLField(
        blank=True, 
        validators=[URLValidator()],
        help_text="Personal website/portfolio.")
    linkedin = models.URLField(
        blank=True, 
        validators=[URLValidator()], 
        help_text="LinkedIn URL")
    github = models.URLField(
        blank=True, 
        validators=[URLValidator()], 
        help_text="GitHub URL")
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        validators=[phone_validator])
    resume = models.FileField(
        upload_to="resumes/%Y/%m/",
        validators=[max_file_size_mb(5), allowed_extensions("pdf", "docx")],
        blank=True, null=True, help_text="Upload CV (PDF/DOCX, max 5 MB).")
    skills = models.ManyToManyField(
        Skill, 
        blank=True, 
        related_name="profiles",
        help_text="Skills the candidate possesses.")

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"

    def __str__(self):
        return f"Profile: {self.user.email}"

class Experience(UUIDModel, TimeStampedModel):
    profile = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE, 
        related_name="experiences")
    company = models.CharField(max_length=160)
    title = models.CharField(max_length=160)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "experience"
        verbose_name_plural = "experiences"
        indexes = [models.Index(fields=["profile", "start_date"], name="exp_profile_start_idx")]

class Education(UUIDModel, TimeStampedModel):
    profile = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE,
        related_name="education")
    institution = models.CharField(max_length=160)
    degree = models.CharField(max_length=160, blank=True)
    field_of_study = models.CharField(max_length=160, blank=True)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "education"
        verbose_name_plural = "education histories"
        indexes = [models.Index(fields=["profile", "start_year"], name="edu_profile_start_idx")]
