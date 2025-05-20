from django.http import Http404
from rest_framework import viewsets, mixins, permissions
from .models import GameAccount
from .serializers import AccountSerialzer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import NumberPairSerializer
from .utils import PSP

class AccountViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin):
    queryset = GameAccount.objects.all()
    serializer_class = AccountSerialzer
    permission_classes = [permissions.AllowAny]
    
    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            # Если запись не найдена, создаем новую
            user_id = self.kwargs.get('pk')
            if not GameAccount.objects.filter(id=user_id).exists():
                serializer = self.get_serializer(data={
                    'user_id': user_id,
                    'id': user_id
                    # Добавьте другие обязательные поля по умолчанию
                })
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                return serializer.instance
            raise

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
class CompareNumbersAPI(APIView):
    def post(self, request):
        serializer = NumberPairSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        num1 = serializer.validated_data['num1']
        num2 = serializer.validated_data['num2']

        # Генерируем два случайных числа
        gen1 = PSP(num1)
        gen2 = PSP(num2)

        # Проверяем условия
        user_pair = {num1, num2}
        gen_pair = {gen1, gen2}

        if user_pair == gen_pair:
            result = 0  # полное совпадение
        elif (num1 == gen1) or (num2 == gen2) or (num1 == gen2) or (num2 == gen1):
            result = 1  # частичное совпадение
        else:
            result = 2  # нет совпадений

        return Response({
            "generated_numbers": [gen1, gen2],
            "result": result
        })