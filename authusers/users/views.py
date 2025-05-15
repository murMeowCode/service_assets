from django.core.mail import send_mail
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import UserConfirmSerializer,CustomTokenObtainPairSerializer
from .permissions import IsAdministrator
from authusers.settings import EMAIL_HOST_USER

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