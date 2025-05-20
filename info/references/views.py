from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import RoleSerializer, VipSerializer
from .models import Role, VipStatus

class RoleListAPIView(ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    
class VipAPIView(RetrieveAPIView):
    queryset = VipStatus.objects.all()
    serializer_class = VipSerializer
