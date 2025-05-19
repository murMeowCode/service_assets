from django.http import Http404
from rest_framework import viewsets, mixins, permissions
from .models import GameAccount
from .serializers import AccountSerialzer

class AccountViewSet(viewsets.GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin):
    queryset = GameAccount.objects.all()
    serializer_class = AccountSerialzer
    permission_classes = [permissions.IsAuthenticated]
    
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            # Если запись не найдена, создаем новую
            serializer = self.get_serializer(data={
                'user_id': request.user.id,
                'id' : request.user.id
                # Добавьте другие обязательные поля по умолчанию
            })
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            instance = serializer.instance
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)