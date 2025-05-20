from djoser.serializers import UserCreateSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User 
from djoser.serializers import UserSerializer  # Или другой базовый сериализатор
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()

class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','balance','balance_virtual')
        read_only_fields = ('id','username')

class CustomUserUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='first_name', required=False)
    firstname = serializers.CharField(source='last_name', required=False)
    patronymic = serializers.CharField(source='father_name', required=False)
    birthdate = serializers.CharField(required=False)  # Принимаем любую строку
    vip_level = serializers.IntegerField(required=False)
    
    class Meta:
        model = User
        fields = ['name', 'firstname', 'patronymic', 'birthdate','vip_level']
    
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
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.father_name = validated_data.get('father_name', instance.father_name)
        
        # Обрабатываем специальные поля
        if 'birthdate' in validated_data:
            instance.birthday = validated_data['birthdate']
        
        # Добавляем обработку vip_level
        if 'vip_level' in validated_data:
            instance.vip_level = validated_data['vip_level']
        
        instance.save()
        return instance

class CustomUserCreateSerializer(UserCreateSerializer):
    birthday = serializers.DateField(required=True)
    father_name = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    is_root = serializers.BooleanField(required=False)
    balance = serializers.FloatField(required=False)
    balance_virtual = serializers.FloatField(required=False)
    vip_level = serializers.IntegerField(required=False)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = UserCreateSerializer.Meta.fields + ('first_name','last_name','father_name','birthday','is_root', "balance", 'balance_virtual', 'vip_level')

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