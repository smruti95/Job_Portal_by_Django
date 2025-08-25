from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower
from django.core.validators import EmailValidator
from common.models import TimeStampedModel, UUIDModel
from common.validators import phone_validator

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra):
        if not email:
            raise ValueError("Email must be provided")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra):
        extra.setdefault("is_staff", False)
        extra.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra)

    def create_superuser(self, email, password=None, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra)

class User(UUIDModel, TimeStampedModel, AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, 
        verbose_name="email address",
        help_text="Primary email used to sign in.",
        validators=[EmailValidator()]
    )
    first_name = models.CharField(
        max_length=150, blank=True,
        verbose_name="first name", 
        help_text="User first name.")
    last_name = models.CharField(
        max_length=150, 
        blank=True,
        verbose_name="last name", 
        help_text="User last name.")
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        validators=[phone_validator],
        verbose_name="phone number", 
        help_text="User contact number.")
    is_recruiter = models.BooleanField(
        default=False, db_index=True,
        verbose_name="recruiter?", 
        help_text="Marks a user as recruiter/employer.")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        indexes = [
            models.Index(Lower("email"), name="accounts_user_email_ci_idx"),
        ]
        constraints = [
            # Case-insensitive unique email
            models.UniqueConstraint(Lower("email"), name="accounts_user_email_ci_uniq"),
        ]

    def __str__(self):
        return self.email
