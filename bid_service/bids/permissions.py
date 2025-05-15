from rest_framework import permissions

class BidPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Просмотр списка: только для аутентифицированных
        if view.action == 'list':
            return request.user.is_authenticated
        # Создание: любой авторизованный юзер
        elif view.action == 'create':
            return request.user.is_authenticated
        # Остальные действия проверяем в has_object_permission
        return True

    def has_object_permission(self, request, view, obj):
        # Админ (role=0) может всё
        if request.user.role == 0:
            return True

        # Просмотр: автор или админ
        if view.action in ['retrieve', 'list']:
            return obj.author == request.user or request.user.role == 0

        # Редактирование/удаление: только админ (role=0)
        if view.action in ['update', 'partial_update']:
            return False  # Запрещаем всем, кроме админа (уже проверили выше)

        # Удаление: только автор и статус pending
        if view.action == 'destroy':
            return obj.author == request.user and obj.status == 'pending'

        return False