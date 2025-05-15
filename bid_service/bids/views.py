from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Bid
from .serializers import BidSerializer
from .permissions import BidPermission
from .tasks import send_notification

class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [BidPermission,IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 0:  # Админ видит всё
            return Bid.objects.all()
        return Bid.objects.filter(author_id=user.id)  # Остальные — только свои

    def perform_create(self, serializer):
        # Автоматически назначаем автора = текущий юзер
        serializer.save(author_id=self.request.user.id)

    def update(self, request, *args, **kwargs):
        if request.user.role != 0:
            raise PermissionDenied("Только администратор может подтверждать заявки!")
        
        instance = self.get_object()
        old_status = instance.status
        response = super().update(request, *args, **kwargs)
        
        # Проверяем, изменился ли статус
        instance.refresh_from_db()
        if old_status != instance.status:
            send_notification(instance)
        
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author_id != request.user.id:
            raise PermissionDenied("Вы не автор этой заявки!")
        if instance.status != 'pending':
            raise PermissionDenied("Можно удалять только заявки в статусе ожидания!")
        return super().destroy(request, *args, **kwargs)