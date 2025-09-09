from rest_framework import permissions


class CoworkingPermission(permissions.BasePermission):
    """
    Админ: полный CRUD во всех моделях.
    Пользователь: только чтение + POST в Booking.
    """
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == "POST" and view.__class__.__name__ == "BookingView":
            return True
        return False
