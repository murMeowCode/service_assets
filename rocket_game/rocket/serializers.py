from rest_framework.serializers import ModelSerializer
from .models import GameAccount
# serializers.py
from rest_framework import serializers

class AccountSerialzer(ModelSerializer):
    class Meta:
        model = GameAccount
        fields = ('__all__')




class NumberPairSerializer(serializers.Serializer):
    num1 = serializers.IntegerField(min_value=1)
    num2 = serializers.IntegerField(min_value=1)