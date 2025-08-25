from django.db import models
from django.db.models.functions import Lower
from django.utils.text import slugify
from common.models import UUIDModel, TimeStampedModel, Activatable
from accounts.models import User
from common.choices import CompanyRole

class Company(UUIDModel, TimeStampedModel, Activatable):
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name="companies_owned",
        verbose_name="owner",
        help_text="Primary owner of the company."
    )
    name = models.CharField(
        max_length=200, 
        db_index=True,
        verbose_name="company name", help_text="Registered company name."
    )
    slug = models.SlugField(
        max_length=220, 
        unique=True, 
        db_index=True,
        verbose_name="slug", 
        help_text="URL-friendly identifier, unique across companies."
    )
    website = models.URLField(
        blank=True, 
        verbose_name="website",
        help_text="Official company website."
    )
    industry = models.CharField(
        max_length=120, 
        blank=True, 
        db_index=True,
        verbose_name="industry", 
        help_text="Industry sector."
    )
    size = models.PositiveIntegerField(
        default=1, 
        verbose_name="company size",
        help_text="Approximate employee count."
    )
    city = models.CharField(
        max_length=120, 
        blank=True
    )
    country = models.CharField(
        max_length=120, 
        blank=True
    )
    about = models.TextField(
        blank=True,
        help_text="Public company description."
    )
    verified = models.BooleanField(
        default=False, 
        db_index=True,
        help_text="Whether the company is verified by the platform."
    )

    class Meta:
        verbose_name = "company"
        verbose_name_plural = "companies"
        indexes = [
            models.Index(Lower("name"), name="companies_name_ci_idx"),
            models.Index(fields=["industry", "country"], name="companies_industry_country_idx"),
        ]
        constraints = [
            models.CheckConstraint(check=~models.Q(name=""), name="companies_name_not_blank"),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:220]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class CompanyMember(UUIDModel, TimeStampedModel):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="members",
        verbose_name="company"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="company_memberships",
        verbose_name="user"
    )
    role = models.CharField(
        max_length=20,
        choices=CompanyRole.choices,
        default=CompanyRole.RECRUITER,
        db_index=True,
        help_text="Membership role within the company."
    )

    class Meta:
        verbose_name = "company member"
        verbose_name_plural = "company members"
        constraints = [
            models.UniqueConstraint(fields=["company", "user"], name="unique_company_user_member"),
        ]

    def __str__(self):
        return f"{self.user.email} @ {self.company.name}"
