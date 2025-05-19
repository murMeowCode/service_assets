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