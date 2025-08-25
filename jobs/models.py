from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.text import slugify
from common.models import UUIDModel, TimeStampedModel, Activatable
from companies.models import Company
from accounts.models import User
from common.choices import ExperienceLevel, EmploymentType, LocationType

class JobCategory(UUIDModel, TimeStampedModel, Activatable):
    name = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        verbose_name="category name",
        help_text="e.g., Software Engineering, Marketing"
    )

    class Meta:
        verbose_name = "job category"
        verbose_name_plural = "job categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Job(UUIDModel, TimeStampedModel, Activatable):
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE,
        related_name="jobs"
    )
    title = models.CharField(
        max_length=255, 
        db_index=True)
    slug = models.SlugField(
        max_length=255, 
        unique=False)  
    description = models.TextField()
    category = models.ForeignKey(
        JobCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="jobs")

    experience_level = models.CharField(
        max_length=50, 
        choices=ExperienceLevel.choices, 
        db_index=True)
    employment_type = models.CharField(
        max_length=50, 
        choices=EmploymentType.choices, 
        db_index=True)
    location_type = models.CharField(
        max_length=50, 
        choices=LocationType.choices, 
        db_index=True
        )

    country = models.CharField(
        max_length=100, 
        blank=True, null=True, 
        db_index=True
        )
    city = models.CharField(
        max_length=100, 
        blank=True, null=True, 
        db_index=True
        )

    min_salary = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True
        )
    max_salary = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True
        )
    application_deadline = models.DateField(help_text="Last date to apply")
    published_at = models.DateTimeField(blank=True, null=True)

    skills = models.ManyToManyField("Skill", related_name="jobs", blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["company", "slug"], name="unique_job_slug_per_company"),
            models.CheckConstraint(
                check=(
                    models.Q(min_salary__lte=models.F("max_salary")) |
                    models.Q(min_salary__isnull=True) |
                    models.Q(max_salary__isnull=True)
                ),
                name="job_min_lte_max_salary"
            )
        ]
        indexes = [
            models.Index(fields=["experience_level", "employment_type"]),
            models.Index(fields=["country", "city"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} @ {self.company.name}"

    def clean(self):
        super().clean()

        # Salary check (friendly error before DB constraint)
        if self.min_salary and self.max_salary and self.min_salary > self.max_salary:
            raise ValidationError("Minimum salary cannot be greater than maximum salary.")

        # Application deadline check
        if self.application_deadline and self.application_deadline < timezone.now().date():
            raise ValidationError("Application deadline cannot be in the past.")

        # Onsite job must have location
        if self.location_type == LocationType.ONSITE and not (self.city and self.country):
            raise ValidationError("Onsite jobs must have both city and country.")

        # Remote job must NOT have city/country
        if self.location_type == LocationType.REMOTE and (self.city or self.country):
            raise ValidationError("Remote jobs should not have city or country filled.")

    def save(self, *args, **kwargs):
        # Generate slug if missing
        if not self.slug:
            self.slug = slugify(self.title)

        # Auto-set published_at when activating
        if self.is_active and not self.published_at:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)


class Skill(UUIDModel, TimeStampedModel):
    name = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        verbose_name="skill",
        help_text="e.g., Python, React, SQL"
    )

    class Meta:
        verbose_name = "skill"
        verbose_name_plural = "skills"
        ordering = ["name"]

    def __str__(self):
        return self.name
