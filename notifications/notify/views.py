from rest_framework import mixins,viewsets
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListBrowse(viewsets.GenericViewSet,
                             mixins.ListModelMixin,
                             mixins.UpdateModelMixin):
    
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(to_user=user.id,seen = False)
    




