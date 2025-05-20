from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import RoleSerializer, VipSerializer
from .models import Role, VipStatus

class RoleListAPIView(ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    
class VipAPIView(RetrieveAPIView):
    lookup_field = 'id'  # Теперь будет искать по полю id
    lookup_url_kwarg = 'id'  # Соответствует имени в URL: vip/<int:id>/
    queryset = VipStatus.objects.all()
    serializer_class = VipSerializer
