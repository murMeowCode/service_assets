from django.core.mail import send_mail
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import UpdateAPIView
from .models import User
from rest_framework.views import APIView
from .serializers import UserConfirmSerializer,CustomTokenObtainPairSerializer,BalanceSerializer, CustomUserCreateSerializer, CustomUserUpdateSerializer
from .permissions import IsAdministrator
from authusers.settings import EMAIL_HOST_USER
from djoser.views import UserViewSet
from rest_framework.decorators import action
import logging

logger = logging.getLogger(__name__)  # Создаём логгер для текущего модуля

class CustomUserViewSet(UserViewSet):
    permission_classes = [IsAuthenticated]
        
    @action(detail=False, methods=['get', 'patch'], url_path='me')
    def me(self, request, *args, **kwargs):
        if request.method == 'PATCH':
            serializer = CustomUserUpdateSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            
            serializer.is_valid(raise_exception=True)
            
            user = serializer.save()
            
            return Response(serializer.data)
            
        serializer = CustomUserCreateSerializer(request.user)  # Для GET оставляем старый
        return Response(serializer.data)
    
class PendingUsersViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin,
                          mixins.UpdateModelMixin):
    queryset = User.objects.filter(is_active = False)
    serializer_class = UserConfirmSerializer
    permission_classes = [IsAdministrator]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Получаем значение поля action из данных запроса или сериализатора
        action = serializer.validated_data.get('action')

        # Формируем тему и текст письма в зависимости от action
        if action == 'accept':
            subject = 'Заявка подтверждена'
            message = 'Ваша заявка на регистрацию с правами администратора подтверждена.'
        else:
            subject = 'Заявка отклонена'
            message = 'Ваша заявка на регистрацию с правами администратора отклонена.'

        # Получаем email пользователя, например, из instance или serializer
        user_email = instance.email

        # Отправляем письмо
        send_mail(
            subject,
            message,
            EMAIL_HOST_USER,
            [user_email],
            fail_silently=False,
        )

        return Response(serializer.data)
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    

class BalanceAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = BalanceSerializer

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        action = request.data.get('action')
        value_type = request.data.get('value_type')
        value = request.data.get('value', 0)
        
        try:
            value = float(value)
            if value <= 0:
                raise ValueError("Value must be positive")
        except (TypeError, ValueError):
            return Response(
                {"error": "Invalid value. Must be a positive number."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if action == 'in':
            if value_type == 'real':
                user.balance += value
            elif value_type == 'virtual':
                user.balance_virtual += value
            else:
                return Response(
                    {"error": "Invalid value_type for 'in' action"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.save()
            return Response({"status": "success", "new_balance": user.balance, "new_virtual_balance": user.balance_virtual})

        elif action == 'out':
            if value_type == 'real':
                if user.balance < value:
                    return Response(
                        {"error": "Insufficient real balance"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                user.balance -= value
            elif value_type == 'virtual':
                if user.balance_virtual < value:
                    return Response(
                        {"error": "Insufficient virtual balance"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                user.balance_virtual -= value
            else:
                return Response(
                    {"error": "Invalid value_type for 'out' action"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.save()
            return Response({"status": "success", "new_balance": user.balance, "new_virtual_balance": user.balance_virtual})

        elif action == 'convert':
            if value_type != 'real':
                return Response(
                    {"error": "Conversion only allowed from real to virtual"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if user.balance < value:
                return Response(
                    {"error": "Insufficient real balance for conversion"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user.balance -= value
            bonus = value * 0.05  # 5% bonus
            user.balance_virtual += value + bonus
            user.save()
            return Response({
                "status": "success",
                "converted": value,
                "bonus": bonus,
                "new_balance": user.balance,
                "new_virtual_balance": user.balance_virtual
            })

        else:
            return Response(
                {"error": "Invalid action. Allowed: 'in', 'out', 'convert'"},
                status=status.HTTP_400_BAD_REQUEST
            )

class BalanceAPIView(APIView):  # Изменено с UpdateAPIView на APIView
    serializer_class = BalanceSerializer

    def patch(self, request, *args, **kwargs):
        user = request.user
        action = request.data.get('action')
        value_type = request.data.get('value_type')
        value = request.data.get('value', 0)
        
        try:
            value = float(value)
            if value <= 0:
                raise ValueError("Value must be positive")
        except (TypeError, ValueError):
            return Response(
                {"error": "Invalid value. Must be a positive number."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if action == 'in':
            if value_type == 'real':
                user.balance += value
            elif value_type == 'virtual':
                user.balance_virtual += value
            else:
                return Response(
                    {"error": "Invalid value_type for 'in' action"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.save()
            return Response({
                "status": "success",
                "new_balance": user.balance,
                "new_virtual_balance": user.balance_virtual
            })

        elif action == 'out':
            if value_type == 'real':
                if user.balance < value:
                    return Response(
                        {"error": "Insufficient real balance"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                user.balance -= value
            elif value_type == 'virtual':
                if user.balance_virtual < value:
                    return Response(
                        {"error": "Insufficient virtual balance"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                user.balance_virtual -= value
            else:
                return Response(
                    {"error": "Invalid value_type for 'out' action"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.save()
            return Response({
                "status": "success",
                "new_balance": user.balance,
                "new_virtual_balance": user.balance_virtual
            })

        elif action == 'convert':
            if value_type != 'real':
                return Response(
                    {"error": "Conversion only allowed from real to virtual"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if user.balance < value:
                return Response(
                    {"error": "Insufficient real balance for conversion"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user.balance -= value
            bonus = value * 0.05
            user.balance_virtual += value + bonus
            user.save()
            return Response({
                "status": "success",
                "converted": value,
                "bonus": bonus,
                "new_balance": user.balance,
                "new_virtual_balance": user.balance_virtual
            })

        # Добавлено: возврат ошибки, если action не распознан
        return Response(
            {"error": "Invalid action. Allowed: 'in', 'out', 'convert'"},
            status=status.HTTP_400_BAD_REQUEST
        )