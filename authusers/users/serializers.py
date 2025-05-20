from djoser.serializers import UserCreateSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User 
from djoser.serializers import UserSerializer  # Или другой базовый сериализатор
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()

class CustomUserUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='first_name', required=False)
    firstname = serializers.CharField(source='last_name', required=False)
    patronymic = serializers.CharField(source='father_name', required=False)
    birthdate = serializers.CharField(required=False)  # Принимаем любую строку
    
    class Meta:
        model = User
        fields = ['name', 'firstname', 'patronymic', 'birthdate']
    
    def validate_birthdate(self, value):
        """Парсим дату в разных форматах"""
        if not value:
            return None
            
        try:
            # Пробуем ISO формат (2004-01-23T00:00:00Z)
            return datetime.fromisoformat(value.replace('Z', '+00:00')).date()
        except ValueError:
            try:
                # Пробуем простой формат даты (2004-01-23)
                return datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise serializers.ValidationError(
                    'Неправильный формат даты. Используйте YYYY-MM-DD или ISO формат.'
                )
    
    def update(self, instance, validated_data):
        # Обновляем стандартные поля
        if 'first_name' in validated_data:
            instance.first_name = validated_data['first_name']
        if 'last_name' in validated_data:
            instance.last_name = validated_data['last_name']
        if 'father_name' in validated_data:
            instance.father_name = validated_data['father_name']
        
        # Особый случай для даты рождения
        if 'birthdate' in validated_data:
            instance.birthday = validated_data['birthdate']
        
        instance.save()
        return instance

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