from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.TextChoices):
    SEEKER = "SEEKER", "Job Seeker"
    EMPLOYER = "EMPLOYER", "Employer"
    ADMIN = "ADMIN", "Administrator"


class User(AbstractUser):
    role = models.CharField(max_length=20, choices=Role.choices)
    is_verified = models.BooleanField(default=False)

    # Remove username field, use email instead
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
