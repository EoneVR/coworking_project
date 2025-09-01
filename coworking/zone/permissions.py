from rest_framework import permissions


class CoworkingPermission(permissions.BasePermission):
    """
    Админ: полный CRUD во всех моделях.
    Пользователь: только чтение везде + POST в Booking.
    """
    def has_permission(self, request, view):
        # Админам всё разрешено
        if request.user and request.user.is_staff:
            return True

        # Чтение разрешено всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Обычному пользователю разрешаем POST только в BookingView
        if request.method == "POST" and view.__class__.__name__ == "BookingView":
            return True

        # Всё остальное запрещено
        return False