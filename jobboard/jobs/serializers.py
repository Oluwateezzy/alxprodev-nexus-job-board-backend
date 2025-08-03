# jobs/serializers.py
from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=Role.choices)

    class Meta:
        model = User
        fields = ["id", "email", "role", "is_verified", "date_joined"]
        extra_kwargs = {
            "password": {"write_only": True},
            "is_verified": {"read_only": True},
            "date_joined": {"read_only": True},
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"
        read_only_fields = ["user"]


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"
        read_only_fields = ["created_by"]


class JobPostingSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source="company", write_only=True
    )

    class Meta:
        model = JobPosting
        fields = "__all__"
        read_only_fields = ["date_posted", "views_count"]


class ApplicationSerializer(serializers.ModelSerializer):
    job = JobPostingSerializer(read_only=True)
    job_id = serializers.PrimaryKeyRelatedField(
        queryset=JobPosting.objects.all(), source="job", write_only=True
    )
    user = UserSerializer(read_only=True)

    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ["user", "submitted_at", "updated_at"]


class BookmarkSerializer(serializers.ModelSerializer):
    job = JobPostingSerializer(read_only=True)
    job_id = serializers.PrimaryKeyRelatedField(
        queryset=JobPosting.objects.all(), source="job", write_only=True
    )

    class Meta:
        model = Bookmark
        fields = "__all__"
        read_only_fields = ["user", "created_at"]
