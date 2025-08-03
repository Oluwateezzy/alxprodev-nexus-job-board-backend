# jobs/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Role(models.TextChoices):
    SEEKER = "SEEKER", "Job Seeker"
    EMPLOYER = "EMPLOYER", "Employer"
    ADMIN = "ADMIN", "Administrator"


class EmploymentType(models.TextChoices):
    FULL_TIME = "FULL_TIME", "Full Time"
    PART_TIME = "PART_TIME", "Part Time"
    CONTRACT = "CONTRACT", "Contract"
    TEMPORARY = "TEMPORARY", "Temporary"
    INTERNSHIP = "INTERNSHIP", "Internship"
    VOLUNTEER = "VOLUNTEER", "Volunteer"


class LocationType(models.TextChoices):
    REMOTE = "REMOTE", "Remote"
    HYBRID = "HYBRID", "Hybrid"
    ON_SITE = "ON_SITE", "On Site"


class ApplicationStatus(models.TextChoices):
    APPLIED = "APPLIED", "Applied"
    REVIEWED = "REVIEWED", "Reviewed"
    INTERVIEWED = "INTERVIEWED", "Interviewed"
    REJECTED = "REJECTED", "Rejected"
    OFFERED = "OFFERED", "Offered"


class JobStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    ACTIVE = "ACTIVE", "Active"
    CLOSED = "CLOSED", "Closed"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    contact_info = models.CharField(max_length=255, blank=True, null=True)
    resume_url = models.URLField(blank=True, null=True)
    skills = models.JSONField(default=list)
    education = models.JSONField(default=dict)
    experience = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.user.email}'s Profile"


class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    logo_url = models.URLField(blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    founded_year = models.IntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    verified = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="companies"
    )

    def __str__(self):
        return self.name


class JobPosting(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="job_postings"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    employment_type = models.CharField(max_length=20, choices=EmploymentType.choices)
    salary_range_min = models.FloatField(blank=True, null=True)
    salary_range_max = models.FloatField(blank=True, null=True)
    currency = models.CharField(max_length=3, blank=True, null=True)
    location_type = models.CharField(max_length=20, choices=LocationType.choices)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=JobStatus.choices, default=JobStatus.DRAFT
    )
    views_count = models.IntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=["title", "description"]),
            models.Index(fields=["city", "country"]),
            models.Index(fields=["employment_type"]),
            models.Index(fields=["salary_range_max"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.title} at {self.company.name}"


class Application(models.Model):
    job = models.ForeignKey(
        JobPosting, on_delete=models.CASCADE, related_name="applications"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="applications"
    )
    resume_url = models.URLField()
    cover_letter_url = models.URLField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.APPLIED,
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ["job", "user"]

    def __str__(self):
        return f"{self.user.email}'s application for {self.job.title}"


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    job = models.ForeignKey(
        JobPosting, on_delete=models.CASCADE, related_name="bookmarks"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "job"]

    def __str__(self):
        return f"{self.user.email}'s bookmark for {self.job.title}"
