from rest_framework import permissions


class CustomPermissionClass(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return False

    # This method will only be called for retrieve, update, delete
    def has_object_permission(self, request, view, obj):
        if obj.title.endswith('updated'):
            return False
        return True
