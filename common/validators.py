
import os
from datetime import date
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible


phone_validator = RegexValidator(
    regex=r"^\+?[0-9]{7,15}$",
    message="Enter a valid phone number with 7–15 digits (optionally prefixed by +)."
)


@deconstructible
class MaxFileSizeValidator:
    def __init__(self, max_mb):
        self.max_mb = max_mb

    def __call__(self, file):
        if file.size > self.max_mb * 1024 * 1024:
            raise ValidationError(f"File too large. Max size is {self.max_mb} MB.")

    def __eq__(self, other):
        return isinstance(other, MaxFileSizeValidator) and self.max_mb == other.max_mb


@deconstructible
class AllowedExtensionsValidator:
    def __init__(self, exts):
        self.exts = set(x.lower().lstrip(".") for x in exts)

    def __call__(self, file):
        _, ext = os.path.splitext(file.name)
        if ext.lower().lstrip(".") not in self.exts:
            raise ValidationError(f"Invalid file type. Allowed: {', '.join(self.exts)}")

    def __eq__(self, other):
        return isinstance(other, AllowedExtensionsValidator) and self.exts == other.exts


def max_file_size_mb(max_mb: int):
    return MaxFileSizeValidator(max_mb)


def allowed_extensions(*exts):
    return AllowedExtensionsValidator(exts)


def future_date(value):
    if value and value < date.today():
        raise ValidationError("This date must be today or in the future.")
