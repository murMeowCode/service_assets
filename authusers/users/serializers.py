from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User 



class CustomUserCreateSerializer(UserCreateSerializer):
    ROLE_CHOICES = (
        (0, 'Администратор'),
        (1, 'Пользователь')
    )
    role = serializers.ChoiceField(choices=ROLE_CHOICES, required=True)
    birthday = serializers.DateField(required=True)
    father_name = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = UserCreateSerializer.Meta.fields + ('role','first_name','last_name','father_name','birthday')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])

        is_active = (validated_data['role'] != 0)  # Админ активен не сразу
        
        user = User.objects.create(
            **validated_data,
            is_active=is_active
        )

        return user
    
class UserConfirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','father_name','is_active')
        read_only_fields = ('id', 'username', 'first_name', 'last_name', 'father_name')
