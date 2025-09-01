from rest_framework import permissions


class BookshopPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.user.is_staff == True:
                return True
            else:
                return False
