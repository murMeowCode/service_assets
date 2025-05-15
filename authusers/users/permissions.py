from rest_framework.permissions import BasePermission

class IsAdministrator(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        # Проверяем, что пользователь аутентифицирован и имеет роль администратора
        if user and user.is_authenticated:
            return user.role == 0
        return False
