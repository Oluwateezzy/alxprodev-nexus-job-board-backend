# jobs/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.permissions import IsAdmin, IsEmployer, IsOwner
from .models import *
from .serializers import *
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from auth.models import Role


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    http_method_names = ["get", "post", "put", "delete"]

    def get_permissions(self):
        if self.action in ["create", "update", "destroy"]:
            permission_classes = [permissions.IsAuthenticated, IsEmployer | IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class JobPostingViewSet(viewsets.ModelViewSet):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    filter_backends = [DjangoFilterBackend]
    http_method_names = ["get", "post", "PATCH", "delete"]

    filterset_fields = ["employment_type", "location_type", "city", "country", "status"]

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            permission_classes = [permissions.IsAuthenticated, IsEmployer | IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["post"])
    def publish(self, request, pk=None):
        job = self.get_object()
        job.status = JobStatus.ACTIVE
        job.save()
        return Response({"status": "published"})

    @action(detail=False, methods=["get"])
    def search(self, request):
        query = Q()

        # Location filters
        if location := request.GET.get("location"):
            query &= Q(city__icontains=location) | Q(country__icontains=location)

        # Employment type
        if employment_type := request.GET.get("employment_type"):
            query &= Q(employment_type=employment_type)

        # Salary range
        if min_salary := request.GET.get("min_salary"):
            query &= Q(salary_range_max__gte=min_salary)

        # Full-text search
        if search_term := request.GET.get("q"):
            query &= (
                Q(title__icontains=search_term)
                | Q(description__icontains=search_term)
                | Q(requirements__icontains=search_term)
            )

        jobs = JobPosting.objects.filter(query).select_related("company")
        serializer = self.get_serializer(jobs, many=True)
        return Response(serializer.data)


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    http_method_names = ["get", "post", "PATCH", "delete"]

    def get_queryset(self):
        # Handle schema generation (when user is AnonymousUser)
        if (
            getattr(self, "swagger_fake_view", False)
            or not self.request.user.is_authenticated
        ):
            return super().get_queryset()

        # Employers see applications for their jobs
        if self.request.user.role == Role.EMPLOYER:
            return (
                super()
                .get_queryset()
                .filter(job__company__created_by=self.request.user)
            )
        # Users see their own applications
        return super().get_queryset().filter(user=self.request.user)

    def get_permissions(self):
        if self.action in ["create"]:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ["partial_update", "destroy"]:
            permission_classes = [permissions.IsAuthenticated, IsOwner | IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    http_method_names = ["get", "post", "PATCH", "delete"]

    def get_queryset(self):
        # Handle schema generation (when user is AnonymousUser)
        if (
            getattr(self, "swagger_fake_view", False)
            or not self.request.user.is_authenticated
        ):
            return super().get_queryset()

        return super().get_queryset().filter(user=self.request.user)

    def get_permissions(self):
        if self.action in ["create", "list", "retrieve", "destroy"]:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, IsOwner | IsAdmin]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
