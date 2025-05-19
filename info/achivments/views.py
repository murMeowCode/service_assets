from rest_framework import generics
from .models import Achivments, AchivmentsUser
from .serializers import AchivmentsSerializer

class AchivmentsListView(generics.ListAPIView):
    queryset = Achivments.objects.all()
    serializer_class = AchivmentsSerializer

class UserAchivmentsListView(generics.ListAPIView):
    serializer_class = AchivmentsSerializer

    def get_queryset(self):
        user_id = self.request.user.id

        # Фильтруем AchivmentsUser по user_id и берем связанные ачивки
        achivments_ids = AchivmentsUser.objects.filter(user_id=user_id).values_list('achivments_id', flat=True)

        # Возвращаем queryset ачивок пользователя
        return Achivments.objects.filter(id__in=achivments_ids)