from djoser.serializers import UserCreateSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User 



class CustomUserCreateSerializer(UserCreateSerializer):
    birthday = serializers.DateField(required=True)
    father_name = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    is_root = serializers.BooleanField(required=False)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = UserCreateSerializer.Meta.fields + ('first_name','last_name','father_name','birthday','is_root')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])

        user = User.objects.create(
            **validated_data
        )

        return user

    
class UserConfirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','father_name','is_active')
        read_only_fields = ('id', 'username', 'first_name', 'last_name', 'father_name')

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)  # Получаем стандартный токен
        
        # Добавляем кастомные поля в payload токена
        token['user_id'] = user.id
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['father_name'] = user.father_name
        
        return token
    
class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','balance','balance_virtual')
        read_only_fields = ('id','username')