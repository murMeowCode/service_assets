from rest_framework import serializers
from .models import Achivments

class AchivmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achivments
        fields = ['id', 'title', 'description']
