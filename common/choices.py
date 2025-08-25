
from django.db import models

class EmploymentType(models.TextChoices):
    FULL_TIME = "FULL_TIME", "Full time"
    PART_TIME = "PART_TIME", "Part time"
    CONTRACT  = "CONTRACT",  "Contract"
    INTERN    = "INTERN",    "Internship"
    TEMP      = "TEMP",      "Temporary"

class ExperienceLevel(models.TextChoices):
    ENTRY   = "ENTRY",   "Entry"
    MID     = "MID",     "Mid"
    SENIOR  = "SENIOR",  "Senior"
    LEAD    = "LEAD",    "Lead"

class LocationType(models.TextChoices):
    ONSITE = "ONSITE", "On-site"
    REMOTE = "REMOTE", "Remote"
    HYBRID = "HYBRID", "Hybrid"

class ApplicationStatus(models.TextChoices):
    SUBMITTED = "SUBMITTED", "Submitted"
    UNDER_REVIEW = "UNDER_REVIEW", "Under review"
    INTERVIEW = "INTERVIEW", "Interview"
    OFFER = "OFFER", "Offer extended"
    REJECTED = "REJECTED", "Rejected"

class CompanyRole(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    RECRUITER = "RECRUITER", "Recruiter"

class NotificationType(models.TextChoices):
    SYSTEM = "SYSTEM", "System"
    APPLICATION = "APPLICATION", "Application"
    JOB = "JOB", "Job"
