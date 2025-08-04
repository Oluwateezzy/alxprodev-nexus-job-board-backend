# jobboard/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import redirect
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Job Board API",
        default_version="v1",
        description="API documentation for Job Board Platform",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@jobboard.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],
)

# Helper functions
def favicon_view(request):
    return HttpResponse(status=204)  # No Content

def accounts_login_redirect(request):
    return redirect('/api/docs/')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("auth.urls")),
    path("api/", include("jobs.urls")),
    path(
        "api/docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # Handle common 404s
    path("favicon.ico", favicon_view, name="favicon"),
    path("accounts/login/", accounts_login_redirect, name="accounts-login-redirect"),
]
