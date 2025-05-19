from rest_framework.serializers import ModelSerializer
from .models import GameAccount

class AccountSerialzer(ModelSerializer):
    class Meta:
        model = GameAccount
        fields = ('__all__')
