from rest_framework import permissions
from auth.models import Role


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Role.ADMIN


class IsEmployer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Role.EMPLOYER


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
