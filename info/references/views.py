from rest_framework.generics import ListAPIView
from .serializers import RoleSerializer
from .models import Role

class RoleListAPIView(ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
