from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"companies", CompanyViewSet)
router.register(r"jobs", JobPostingViewSet)
router.register(r"applications", ApplicationViewSet)
router.register(r"bookmarks", BookmarkViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
