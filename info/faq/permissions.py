from rest_framework import permissions

class OnlyAdminCreate(permissions.BasePermission):
    """
    Разрешает GET всем, а POST только пользователям с role == 0.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # Разрешаем GET, HEAD, OPTIONS всем
            return True
        if request.method == 'POST':
            # Для создания разрешаем только если роль пользователя 0
            return hasattr(request.user, 'role') and request.user.role == 0
        # Для остальных методов запрещаем
        return False
