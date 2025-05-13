from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
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
        if validated_data['role'] == 1:
            user = User.objects.create(
                **validated_data,
                is_active=False
            )
        else:
            user = User.objects.create(
                **validated_data,
                is_active=True
            )

        return user
