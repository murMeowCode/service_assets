from rest_framework.serializers import ModelSerializer
from .models import Role, VipStatus

class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = ('__all__')
        
class VipSerializer(ModelSerializer):
    class Meta:
        model = VipStatus
        fields = ('__all__')